import sys
from subprocess import call
import os
import warnings

if __name__ == "__main__":
    import tcl_actions
    import graphics_actions
else:
    import molywood.tcl_actions as tcl_actions
    import molywood.graphics_actions as graphics_actions


class Script:
    """
    Main class that will combine all information
    and render the movie (possibly with multiple
    panels, overlays etc.)
    """
    allowed_globals = ['global', 'layout']
    allowed_params = {'global': ['fps', 'keepframes', 'draft', 'name', 'render', 'restart'],
                      'layout': ['columns', 'rows'],
                      '_default': ['visualization', 'structure', 'trajectory', 'position', 'resolution',
                                   'pdb_code', 'after', 'contour', 'ambient_occlusion', 'draft']}
    
    def __init__(self, scriptfile=None):
        self.name = 'movie'
        self.scenes = []
        self.directives = {}
        self.fps = 20
        self.draft, self.do_render, self.keepframes, self.restart, self.parallel = False, True, False, False, False
        self.scriptfile = scriptfile
        self.vmd, self.remove, self.compose, self.convert = 4 * [None]
        self.setup_os_commands()
        if self.scriptfile:
            self.from_file()

    def render(self):
        """
        The final fn that renders the movie (runs
        the TCL script, then uses combine and/or
        ffmpeg to assemble the movie frame by frame)
        :return: None
        """
        def render_scene(script_and_scene):  # the part below controls TCL/VMD rendering
            """
            This fn encapsulates the whole scene-rendering
            protocol only to allow for parallelization with
            the generic Pool.map() approach
            :param script_and_scene: tuple, contains one Script and one Scene instance
            :return: None
            """
            script, scn = script_and_scene
            print("Now rendering scene: {}".format(scn.alias))
            tcl_script = scn.tcl()  # this generates the TCL code, below we save it as script and run VMD
            if scn.run_vmd:
                with open('script_{}.tcl'.format(scn.alias), 'w') as out:
                    out.write(tcl_script)
                ddev = '-dispdev none' if not scn.draft else ''
                if not script.do_render and not scn.draft:
                    raise RuntimeError("render=false is only compatible with draft=true")
                os.system('{} {} -e script_{}.tcl -startup "" 2>&1 | grep -v "Rendering Progress" | '
                          'tee {}_vmdlog.moly | grep "[05].dat"'.format(script.vmd, ddev, scn.alias, scn.alias))
                if script.do_render:
                    if os.name == 'posix':
                        os.system('for i in $(ls {}-*tga); do convert $i $(echo $i | sed "s/tga/png/g"); '
                                  'rm $i; done >/dev/null 2>&1'.format(scn.name))
                    else:
                        to_convert = [x for x in os.listdir('.') if x.startswith(scn.name) and x.endswith('tga')]
                        for tgafile in to_convert:
                            pngfile = tgafile.replace('tga', 'png')
                            call('{} {} {}'.format(script.convert, tgafile, pngfile))
                if not scn.draft:
                    if os.name == 'posix':
                        os.system('for i in $(ls {}-[0-9]*dat); do rm $i; done >/dev/null 2>&1'.format(scn.name))
                    else:
                        os.system('del {}-*dat'.format(scn.name))
            for action in scn.actions:
                action.generate_graph()  # here we generate matplotlib figs on-the-fly
        
        if not self.parallel:
            for scene in self.scenes:
                render_scene((self, scene))
        else:
            from multiprocessing import Pool
            p = Pool()
            p.map(render_scene, [(self, sc) for sc in self.scenes])
        # at this stage, each scene should have all its initial frames rendered
        if self.do_render:
            graphics_actions.postprocessor(self)
            os.system('ffmpeg -y -framerate {fps} -i {n}-%d.png -profile:v high -crf 20 -pix_fmt yuv420p '
                      '-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" {n}.mp4 > {n}_ffmpeglog.moly '
                      '2>&1'.format(fps=self.fps, n=self.name))
        if not self.keepframes:
            # if any([x for x in os.listdir('.') if x.endswith('log.moly')]):
            #     os.system('{} *log.moly >/dev/null 2>&1'.format(self.remove))
            for sc in self.scenes:
                if '/' in sc.name or '\\' in sc.name or '~' in sc.name:
                    raise RuntimeError('For security reasons, cleanup of scenes that contain path-like elements '
                                       '(slashes, backslashes, tildes) is prohibited.\n\n'
                                       'Error triggered by: {}'.format(sc.name))
                else:
                    if any([x for x in os.listdir('.') if x.startswith(sc.name) and x.endswith('png')]):
                        os.system('{} {}-[0-9]*.png >/dev/null 2>&1'.format(self.remove, sc.name))
                    if any([x for x in os.listdir('.') if x.startswith('overlay') and x.endswith('png')
                            and sc.name in x]):
                        os.system('{} overlay[0-9_]*-{}-[0-9]*.png >/dev/null 2>&1'.format(self.remove, sc.name))
                    if any([x for x in os.listdir('.') if x.startswith('script') and x.endswith('tcl')
                            and sc.name in x]):
                        os.system('{} script_{}.tcl >/dev/null 2>&1'.format(self.remove, sc.name))
            if '/' in self.name or '\\' in self.name or '~' in self.name:
                raise RuntimeError('For security reasons, cleanup of scenes that contain path-like elements '
                                   '(slashes, backslashes, tildes) is prohibited.\n\n'
                                   'Error triggered by: {}'.format(self.name))
            else:
                if any([x for x in os.listdir('.') if x.startswith(self.name) and x.endswith('png')]):
                    os.system('{} {}-[0-9]*.png >/dev/null 2>&1'.format(self.remove, self.name))
    
    def show_script(self):
        """
        Shows a sequence of scenes currently
        buffered in the object for rendering;
        mostly for debugging purposes
        :return: None
        """
        for subscript in self.scenes:
            print('\n\n\tScene {}: \n\n'.format(subscript.name))
            subscript.show_script()

    def from_file(self):
        """
        Reads the full movie script from an input file
        and runs parser/setter functions
        :return: None
        """
        script = [line.strip() for line in open(self.scriptfile, 'r')]
        current_subs = ['_default']
        subscripts = {current_subs[0]: []}
        multiline = None
        master_setup = []
        for line in script:
            excl = line.find('!')
            if excl >= 0:
                line = line[:excl].strip()
            if line.startswith('#'):  # beginning of a subscript
                current_subs = [sub.strip() for sub in line.strip('#').strip().split(',')]
                for sub in current_subs:
                    if sub not in subscripts.keys():
                        subscripts[sub] = []
            elif line.startswith('$'):  # global directives
                master_setup.append(line.strip('$').strip())
            elif line:  # regular content of subscript
                if line.startswith('{'):  # with a possibility of multi-actions wrapped into curly brackets
                    multiline = ' ' + line
                elif multiline and not line.strip().endswith('}'):
                    multiline += ' ' + line
                elif multiline and line.strip().endswith('}'):
                    multiline += ' ' + line
                    for act in multiline.strip('\{\} ').split(';'):
                        if not all(len(x.split('=')) >= 2 for x in Action.split_input_line(act)[1:]):
                            raise RuntimeError("Have you forgotten to add a semicolon in action: \n\n{}?\n".format(act))
                    for sub in current_subs:  # TODO if more than 1 '=', check if others are in quot marks
                        subscripts[sub].append(multiline)
                    multiline = None
                else:
                    for sub in current_subs:
                        subscripts[sub].append(line)
        if multiline:
            raise RuntimeError("Error: not all curly brackets {} were closed, revise your input")
        Script.allowed_globals.extend(list(subscripts.keys()))
        for sc in subscripts.keys():
            Script.allowed_params[sc] = Script.allowed_params['_default']
        self.directives = self.parse_directives(master_setup)
        self.scenes = self.parse_scenes(subscripts)
        self.prepare()
    
    def setup_os_commands(self):
        """
        Paths to VMD, imagemagick utilities, OS-specific
        versions of rm/del, ls/dir, which/where, ffmpeg etc.
        have to be determined to allow for Linux/OSX/Win
        compatibility. NOTE: compatibility with Windows might be
        a future feature, currently not well-tested
        :return: None
        """
        if os.name == 'posix':
            self.remove = 'rm'
            self.vmd = 'vmd'
            self.compose, self.convert = 'composite', 'convert'
            if os.system('which ffmpeg >/dev/null 2>&1') != 0:
                raise RuntimeError("ffmpeg was not found on your machine; try installing it using e.g. "
                                   "sudo apt-get install ffmpeg")
            if os.system('which vmd >/dev/null 2>&1') != 0:
                raise RuntimeError("vmd was not found on your machine; look up the documentation and make sure it was"
                                   "installed properly")
            if os.system('which convert >/dev/null 2>&1') != 0:
                raise RuntimeError("imagemagick was not found on your machine; try installing it using e.g. "
                                   "sudo apt-get install imagemagick")
        elif os.name == 'nt':
            import pathlib
            self.remove = 'del'
            for pfiles in [x for x in os.listdir('C:\\') if x.startswith('Program Files')]:
                for file in pathlib.Path('C:\\{}'.format(pfiles)).glob('**/vmd.exe'):
                    self.vmd = str(file)
            if not self.vmd:
                raise RuntimeError("VMD was not found in any of the Program Files directories, check your installation")
            if call('where ffmpeg') != 0:
                raise RuntimeError('ffmpeg not found, please make sure it was added to the system path during '
                                   'installation (see README)')
            if call('where magick') == 0:
                self.compose, self.convert = 'magick composite', 'magick convert'
            else:
                raise RuntimeError('imagemagick not found, please make sure it was added to the system path during '
                                   'installation (see README)')
        else:
            raise RuntimeError('OS type could not be detected')
        
    @staticmethod
    def parse_directives(directives):
        """
        Reads global directives that affect
        the main object (layout, fps, draftmode
        etc.) based on $-prefixed entries
        :param directives:
        :return: dict, contains dictionaries of global keyword:value parameters
        """
        dirs = {}
        for directive in directives:
            entries = directive.split()
            if entries[0] not in Script.allowed_globals:
                raise RuntimeError("'{}' is not an allowed global directive. Allowed "
                                   "global directives are: {}".format(entries[0], ", ".join(Script.allowed_globals)))
            dirs[entries[0]] = {}
            for entry in entries[1:]:
                try:
                    key, value = entry.split('=')
                except ValueError:
                    raise RuntimeError("Entries should contain parameters formatted as 'key=value' pairs,"
                                       "'{}' in line '{}' does not follow that specification".format(entry, directive))
                else:
                    allowed = Script.allowed_params[entries[0]]
                    if key not in allowed:
                        raise RuntimeError("'{}' is not a parameter compatible with the directive {}. Allowed "
                                           "parameters include: {}".format(key, entries[0],
                                                                           ", ".join(list(allowed))))
                    dirs[entries[0]][key] = value
        return dirs
    
    def parse_scenes(self, scenes):
        """
        Reads info on individual scenes and initializes
        Scene objects, later to be appended to the Script's
        list of Scenes
        :param scenes: dict, contains scene_name: description bindings
        :return: list, container of Scene objects
        """
        scenelist = []
        pos, res, tcl, py, struct, traj, contour, ao = [1, 1], [1000, 1000], None, None, None, None, None, False
        for sub in scenes.keys():
            if scenes[sub]:
                if sub in self.directives.keys():
                    try:
                        tcl = self.directives[sub]['visualization']
                    except KeyError:
                        pass
                    else:
                        tcl = self.check_path(tcl)
                        tcl = self.check_tcl(tcl)
                    try:
                        pos = [int(x) for x in self.directives[sub]['position'].split(',')]
                    except KeyError:
                        pass
                    try:
                        res = [int(x) for x in self.directives[sub]['resolution'].split(',')]
                    except KeyError:
                        pass
                    try:
                        contour = True if self.directives[sub]['contour'].lower() in ['t', 'y', 'true', 'yes'] else None
                    except KeyError:
                        pass
                    try:
                        ao = True if self.directives[sub]['ambient_occlusion'].lower() in ['t', 'y', 'true', 'yes'] \
                            else False
                    except KeyError:
                        pass
                    try:
                        struct = self.directives[sub]['structure']
                    except KeyError:
                        try:
                            pdb = self.directives[sub]['pdb_code']
                        except KeyError:
                            pass
                        else:
                            if os.name == 'nt':
                                raise RuntimeError("direct download of PDB files currently not supported on Windows")
                            pdb = pdb.upper()
                            if not pdb.upper() + '.pdb' in os.listdir('.'):
                                if os.system('which wget') == 0:
                                    result = os.system('wget https://files.rcsb.org/download/{}.pdb'.format(pdb))
                                elif os.system('which curl') == 0:
                                    result = os.system('curl -O https://files.rcsb.org/download/{}.pdb'.format(pdb))
                                else:
                                    raise RuntimeError("You need wget or curl to directly download PDB files")
                                if result != 0:
                                    raise RuntimeError("Download failed, check your PDB code and internet connection")
                            struct = '{}.pdb'.format(pdb)
                    else:
                        struct = self.check_path(struct)
                    try:
                        traj = self.directives[sub]['trajectory']
                    except KeyError:
                        pass
                    else:
                        traj = self.check_path(traj)
                    try:
                        dft = self.directives[sub]['draft']
                    except KeyError:
                        draft = None
                    else:
                        draft = True if dft.lower() in ['t', 'y', 'true', 'yes'] else False
                    try:
                        after = self.directives[sub]['after']
                    except KeyError:
                        after = None
                    else:
                        if after not in scenes.keys():
                            raise RuntimeError("In after={}, {} does not correspond to any other scene "
                                               "in the input".format(after, after))
                    scenelist.append(Scene(self, sub, tcl, res, pos, struct, traj, after, contour, ao, draft))
                    for action in scenes[sub]:
                        scenelist[-1].add_action(action)
        return scenelist

    def prepare(self):
        """
        Once text input is parsed, this fn sets
        global parameters such as fps, draft mode
        or whether to keep frames
        :return: None
        """
        try:
            self.fps = float(self.directives['global']['fps'])
        except KeyError:
            pass
        try:
            self.draft = True if self.directives['global']['draft'].lower() in ['y', 't', 'yes', 'true'] else False
        except KeyError:
            pass
        for scene in self.scenes:
            if scene.draft is None:
                scene.draft = self.draft
        try:
            self.do_render = False if self.directives['global']['render'].lower() in ['n', 'f', 'no', 'false'] else True
        except KeyError:
            pass
        try:
            self.keepframes = True if self.directives['global']['keepframes'].lower() in ['y', 't', 'yes', 'true'] \
                else False
        except KeyError:
            pass
        try:
            self.name = self.directives['global']['name']
        except KeyError:
            pass
        try:
            self.restart = True if self.directives['global']['restart'].lower() in ['y', 't', 'yes', 'true'] else False
        except KeyError:
            pass
        for scene in self.scenes:
            scene.calc_framenum()
        for scene in self.scenes:
            scene.merge_after()  # TODO enable working with many molecules (mostly switching of tops)
        try:
            self.parallel = True if self.directives['global']['parallel'].lower() in ['y', 't', 'yes', 'true'] \
                else False
            if self.parallel and len(self.scenes) > 1:
                warn_text = "Currently parallel rendering is only supported for multiple scenes, but only one scene "\
                            "was found in the current run. Will proceed anyway but do not expect speedup"
                warnings.warn(warn_text)
        except KeyError:
            pass
    
    def check_path(self, filename):
        """
        Looks for the specified file in the local
        directory and at the location of the input
        file; raises a RuntimeError if file cannot
        be found
        :param filename: str, path (relative or absolute) of the file to be sought
        :return: None
        """
        if os.path.isfile(filename):
            return filename
        elif not os.path.isfile(filename) and '/' in self.scriptfile:
            prefix = '/'.join(self.scriptfile.split('/')[:-1]) + '/'
            if os.path.isfile(prefix + filename):
                return prefix + filename
            else:
                raise RuntimeError('File {} could not been found neither in the local directory '
                                   'nor in {}'.format(filename, prefix))
        else:
            raise RuntimeError('File {} not found, please make sure there are no typos in the name'.format(filename))
    
    @staticmethod
    def check_tcl(tcl_file):
        """
        If the files to be read by VMD were saved as
        absolute paths and then transferred to another
        machine, this fn will identify missing paths
        and look for the files in the working dir,
        creating another file if needed
        :param tcl_file: str, path to the VMD visualization state
        :return: str, new (or same) path to the VMD visualization state
        """
        inp = [line for line in open(tcl_file)]
        modded = False
        for n in range(len(inp)):
            if inp[n].strip().startswith('mol') and inp[n].split()[1] in ['new', 'addfile'] \
                    and inp[n].split()[2].startswith('/'):
                if not os.path.isfile(inp[n].split()[2]):
                    if os.path.isfile(inp[n].split()[2].split('/')[-1]):
                        print('Warning: absolute path {} was substituted with a relative path to the local file {}; '
                              'the modified .vmd file will be '
                              'backed up'.format(inp[n].split()[2], inp[n].split()[2].split('/')[-1]))
                        inp[n] = ' '.join(inp[n].split()[:2]) + " {} ".format(inp[n].split()[2].split('/')[-1]) \
                                 + ' '.join(inp[n].split()[3:])
                        modded = True
        if modded:
            with open(tcl_file + '.localcopy', 'w') as new_tcl:
                for line in inp:
                    new_tcl.write(line)
            return tcl_file + '.localcopy'
        else:
            return tcl_file
                

class Scene:  # TODO add utils for cryo-em & densities as Highlights
    """
    A Scene instance is restricted to a single
    molecular system; all Scene parameters are
    read as input is parsed.
    """
    def __init__(self, script, name, tcl=None, resolution=(1000, 1000), position=(1, 1),
                 structure=None, trajectory=None, after=None, contour=None, ao=False, draft=False):
        self.script = script
        self.name = name
        self.alias = self.name  # one is permanent, one can be variable
        self.visualization = tcl
        self.actions = []
        self.resolution = resolution
        self.position = position
        self.structure = structure
        self.trajectory = trajectory
        self.contour = contour
        self.draft = draft
        self.ao = ao
        self.functions = []
        self.run_vmd = False
        self.total_frames = 0
        self.tachyon = None
        self.after = after
        self.first_frame = 0
        self.is_overlay = 0
        self.counters = {'hl': 0, 'overlay': 0, 'make_transparent': 0, 'make_opaque': 0, 'rot': 0, 'zoom': 0,
                         'translate': 0}
        self.labels = {'Atoms': [], 'Bonds': []}
    
    def add_action(self, description):
        """
        Adds an action to the subscript
        :param description: str, description of the action
        :return: None
        """
        if not description.strip().startswith('{'):
            self.actions.append(Action(self, description))
        else:
            self.actions.append(SimultaneousAction(self, description.strip('{} ')))

    def show_script(self):
        """
        Shows actions scheduled for rendering
        within the current subscript; mostly
        for debugging purposes
        :return: None
        """
        for action in self.actions:
            print(action)
    
    def calc_framenum(self):
        """
        Once the fps rate is known, we can go through all actions
        and set integer frame counts as needed. Note: some actions
        can be instantaneous (e.g. recenter camera), so that
        not all will have a non-zero framenum. Also, the cumulative
        frame number (for the entire Scene) will be calculated.
        :return: None
        """
        fps = self.script.fps
        cumsum = self.first_frame
        for action in self.actions:
            action.initframe = cumsum
            try:
                action.framenum = int(float(action.parameters['t'])*fps)
            except KeyError:
                action.framenum = 0
            cumsum += action.framenum
        self.total_frames = cumsum
    
    def merge_after(self):
        """
        Re-processes frame numberings, scene
        names etc. if the current Scene is meant
        to follow another Scene (specified by setting
        'after=previous_scene' in the Scene input)
        :return: None
        """
        if self.after:
            ref_scene = [sc for sc in self.script.scenes if sc.alias == self.after][0]
            self.first_frame = ref_scene.total_frames
            self.calc_framenum()
            self.name = ref_scene.name
            
    def tcl(self):
        """
        This is the top-level function that produces
        an executable TCL script based on the corresponding
        action.generate() functions; also, many defaults are
        set here to override VMD's internal settings
        :return: str, the TCL code to be executed
        """
        if self.visualization or self.structure or any([str(act) in Action.actions_requiring_tcl
                                                        for act in self.actions]):
            self.run_vmd = True
            if self.visualization:
                code = [line for line in open(self.visualization, 'r').readlines() if not line.startswith('#')]
                code = ''.join(code)
            elif self.structure:
                code = 'mol new {} type {} first 0 last -1 step 1 filebonds 1 ' \
                       'autobonds 1 waitfor all\n'.format(self.structure, self.structure.split('.')[-1])
                if self.trajectory:
                    code += 'mol addfile {} type {} first 0 last -1 step 1 filebonds 1 ' \
                            'autobonds 1 waitfor all\n'.format(self.trajectory, self.trajectory.split('.')[-1])
                code += 'mol delrep 0 top\nmol representation NewCartoon 0.300000 10.000000 4.100000 0\n' \
                        'mol color Structure\nmol selection {all}\nmol material Opaque\nmol addrep top\n' \
                        'color Display Background white\ndisplay projection Orthographic\n'
            else:
                code = 'color Display Background white\ndisplay projection Orthographic\n'
            code += 'axes location off\nset repnums [list]\ncolor add item Type C yellow\ncolor Type C yellow\n' \
                    'color add item Element C black\ncolor Element C black\n'
            if self.ao:
                code += 'display ambientocclusion on\ndisplay aoambient 0.82\ndisplay aodirect 0.25\n'
                if self.draft:
                    warnings.warn("Warning: Ambient Occlusion will not affect the outcome in the draft mode")
            if not self.draft:
                code += 'render options Tachyon \"$env(TACHYON_BIN)\" -aasamples 12 %s -format ' \
                        'TARGA -o %s.tga -trans_max_surfaces 1 -res {} {}\n'.format(*self.resolution)
            else:
                try:
                    screen_res = str(os.popen("xdpyinfo | grep dimensions | awk '{print $2}'").read().strip()).split(
                        'x')
                    screen_res = [int(x) for x in screen_res]
                except:
                    warnings.warn("Cannot determine actual screen size; make sure your resolution does not exceed "
                                  "screen resolution in the draft mode -- frames might be trimmed otherwise.")
                else:
                    if screen_res[0] < self.resolution[0] or screen_res[1] < self.resolution[1]:
                        raise RuntimeError("In the draft mode, scene resolution ({}x{}) should be smaller than your "
                                           "screen resolution ({}x{}), otherwise the resulting frames might not "
                                           "be sized and shaped properly.".format(*self.resolution, *screen_res))
                code += 'display resize {res}\nafter 100\ndisplay update\nafter 100\ndisplay resize {res}\n' \
                        'display rendermode GLSL\n'.format(res=' '.join(str(x) for x in self.resolution))
            action_code = ''
            for ac in self.actions:
                action_code += ac.generate_tcl()
            if action_code:
                code += action_code
        else:
            code = ''
        if all([ac.already_rendered for ac in self.actions]):
            self.run_vmd = False
            print("Skipping scene {}, all frames have already been rendered".format(self.name))
        return code + '\nexit\n'
        
        
class Action:
    """
    Intended to represent a single action in
    a movie, e.g. a rotation, change of material
    or zoom-in
    """
    
    allowed_params = {'do_nothing': {'t'},
                      'animate': {'frames', 'smooth', 't'},
                      'rotate': {'angle', 'axis', 't', 'sigmoid', 'fraction', 'abruptness'},
                      'translate': {'vector', 't', 'sigmoid', 'fraction', 'abruptness'},
                      'zoom_in': {'scale', 't', 'sigmoid', 'fraction', 'abruptness'},
                      'zoom_out': {'scale', 't', 'sigmoid', 'fraction', 'abruptness'},
                      'make_transparent': {'material', 't', 'sigmoid', 'limit', 'start', 'fraction', 'abruptness'},
                      'highlight': {'selection', 't', 'color', 'mode', 'style', 'alias', 'thickness', 'material',
                                    'abruptness', 'alpha'},
                      'make_opaque': {'material', 't', 'sigmoid', 'limit', 'start', 'fraction', 'abruptness'},
                      'center_view': {'selection'},
                      'show_figure': {'figure', 't', 'datafile', 'dataframes'},
                      'add_overlay': {'figure', 't', 'origin', 'relative_size', 'dataframes',
                                      'aspect_ratio', 'datafile', '2D', 'text', 'textsize', 'sigmoid',
                                      'alpha', 'scene', 'transparent_background', 'textcolor', 'decimal_points',
                                      'movie', 'from', 'length'},
                      'add_label': {'label_color', 'atom_index', 'label', 'text_size', 'alias', 'offset'},
                      'remove_label': {'alias', 'all'},
                      'add_distance': {'selection1', 'selection2', 'label_color', 'text_size', 'alias', 'bead'},
                      'remove_distance': {'alias', 'all'},
                      'fit_trajectory': {'selection', 't', 'axis', 'invert', 'abruptness'}
                      }

    allowed_actions = list(allowed_params.keys())

    actions_requiring_tcl = ['do_nothing', 'animate', 'rotate', 'zoom_in', 'zoom_out', 'make_transparent',
                             'make_opaque', 'center_view', 'add_label', 'remove_label', 'highlight',
                             'fit_trajectory', 'add_distance', 'remove_distance', 'translate']
    
    def __init__(self, scene, description):
        self.scene = scene
        self.description = description
        self.action_type = None
        self.parameters = {}  # will be a dict of action parameters
        self.initframe = None  # contains the initial frame number in the overall movie's numbering
        self.framenum = None  # total frames count for this action
        self.highlights, self.transp_changes, self.rots, self.transl, self.zoom = {}, {}, {}, {}, {}
        self.already_rendered = False
        self.parse(description)
    
    def __repr__(self):
        return self.description.split()[0]
    
    def generate_tcl(self):
        """
        Should yield the TCL code that will
        produce the action in question; in case
        of restarting, checks whether frames have
        been rendered already for this action
        :return: str, TCL code
        """
        
        if set(self.action_type).intersection(set(Action.actions_requiring_tcl)):
            if self.scene.script.restart:
                self.check_if_rendered()
            return tcl_actions.gen_loop(self)
        else:
            self.already_rendered = True
            return ''
        
    def check_if_rendered(self):
        """
        In case of restarting, checks whether frames have
        been rendered already for this action
        :return: None
        """
        if all(['{}-{}.png'.format(self.scene.name, f) in os.listdir('.') or
                '{}-{}.tga'.format(self.scene.name, f) in os.listdir('.')
                for f in range(self.initframe, self.initframe + self.framenum)]):
            if any(['{}-{}.tga'.format(self.scene.name, f) in os.listdir('.')
                   for f in range(self.initframe, self.initframe + self.framenum)]):
                os.system('for i in $(ls {}-*tga); do convert $i $(echo $i | sed "s/tga/png/g"); '
                          'rm $i; done'.format(self.scene.name))
            self.already_rendered = True
        elif all(['{}-{}.png'.format(self.scene.script.name, f) in os.listdir('.')
                 for f in range(self.initframe, self.initframe + self.framenum)]):
            os.system('for i in $(ls {}-*png); do mv $i $(echo $i | sed "s/{}/{}/g"); '
                      'done'.format(self.scene.script.name, self.scene.script.name, self.scene.name))
            self.already_rendered = True
    
    def generate_graph(self):
        """
        Runs external functions that take care of
        on-the-fly rendering of matplotlib graphs
        or copying of external images
        :return: None
        """
        actions_requiring_genfig = ['show_figure', 'add_overlay']
        if set(self.action_type).intersection(set(actions_requiring_genfig)):
            graphics_actions.gen_fig(self)
    
    def parse(self, command, ignore=()):
        """
        Parses a single command from the text input
        and converts into action parameters
        :param command: str, description of the action
        :param ignore: tuple, list of parameters to ignore while parsing
        (these will be stored in special-purpose dicts to avoid interference)
        :return: None
        """
        spl = self.split_input_line(command)
        if spl[0] not in Action.allowed_actions:
            raise RuntimeError("'{}' is not a valid action. Allowed actions "
                               "are: {}".format(spl[0], ', '.join(list(Action.allowed_actions))))
        if not isinstance(self, SimultaneousAction) and spl[0] == "add_overlay":
            if "mode=d" not in spl:
                raise RuntimeError("Overlays can only be added simultaneously with another action, not as"
                                   "a standalone one")
        self.action_type = [spl[0]]
        try:
            new_dict = {prm.split('=')[0]: prm.split('=')[1].strip("'\"") for prm in spl[1:]
                        if prm.split('=')[0] not in ignore}
        except IndexError:
            raise RuntimeError("Line '{}' is not formatted properly; action name should be followed by keyword=value "
                               "pairs, and no spaces should encircle the '=' sign".format(command))
        for par in new_dict:
            if par not in Action.allowed_params[spl[0]]:
                raise RuntimeError("'{}' is not a valid parameter for action '{}'. Parameters compatible with this "
                                   "action include: {}".format(par, spl[0],
                                                               ', '.join(list(Action.allowed_params[spl[0]]))))
        self.parameters.update(new_dict)
        if 't' in self.parameters.keys():
            self.parameters['t'] = self.parameters['t'].rstrip('s')
        if not isinstance(self, SimultaneousAction):
            if spl[0] == 'highlight':
                try:
                    alias = '_' + self.parameters['alias']
                except KeyError:
                    alias = self.scene.counters['hl']
                self.highlights = {'hl{}'.format(alias): self.parameters}
                self.scene.counters['hl'] += 1
            if spl[0] in ['make_transparent', 'make_opaque']:  # TODO check for possible interference
                self.transp_changes = {spl[0]: self.parameters}
                self.scene.counters[spl[0]] += 1
            if spl[0] == 'rotate':
                self.rots = {'rot0': self.parameters}
            if spl[0] == 'translate':
                self.transl = {'translate': self.parameters}
            if spl[0].startswith('zoom_'):
                self.zoom = {'zoom': self.parameters}

    @staticmethod
    def split_input_line(line):
        """
        A modified string splitter that doesn't split
        words encircled in quotation marks; required
        by actions that accept a VMD-compatible
        selection string
        :param line: str, line to be split
        :return: list of strings, contains individual words
        """
        line = line.strip()
        words = []
        open_quotation = False
        previous = 0
        for current, char in enumerate(line):
            if char in ["'", '"']:
                if not open_quotation:
                    open_quotation = True
                else:
                    open_quotation = False
            if (char == ' ' and not open_quotation) or current == len(line) - 1:
                word = line[previous:current+1].strip()
                if word:
                    words.append(word)
                previous = current
        return words
        

class SimultaneousAction(Action):
    """
    Intended to represent a number of actions
    that take place simultaneously (e.g. zoom
    and rotation)
    """
    def __init__(self, scene, description):
        self.overlays = {}  # need special treatment for overlays as there can be many ('overlay0', 'overlay1', ...)
        self.highlights = {}  # the same goes for highlights ('hl0', 'hl1', ...)
        self.transp_changes = {}  # ...and for make_opaque/make_transparent
        super().__init__(scene, description)
        
    def parse(self, command, ignore=()):
        """
        We simply add action parameters to the
        params dict, assuming there will be no
        conflict of names (need to ensure this
        when setting action syntax); this *is*
        a workaround, but should work fine for
        now - might write a preprocessor later
        to pick up and fix any possible issues
        :param command: str, description of the actions
        :param ignore: tuple, list of parameters to ignore while parsing
        :return: None
        """
        actions = [comm.strip() for comm in command.split(';') if comm]
        for action in actions:
            igns = []  # ones that we don't want to be overwritten in the 'parameters' dict
            if action.split()[0] == 'add_overlay':
                self.parse_many(action, self.overlays, 'overlay')
                igns.append('figure')
                igns.append('mode')
                igns.append('alias')
            elif action.split()[0] == 'highlight':
                self.parse_many(action, self.highlights, 'hl')
                igns.append('selection')
                igns.append('mode')
                igns.append('alias')
            elif action.split()[0] in ['make_transparent', 'make_opaque']:
                self.parse_many(action, self.transp_changes, action.split()[0])
                igns.append('fraction')
            elif action.split()[0] == 'rotate':
                self.parse_many(action, self.rots, 'rot')
                igns.append('axis')
                igns.append('fraction')
            elif action.split()[0].startswith('zoom_'):
                self.parse_many(action, self.zoom, 'zoom')
                igns.append('fraction')
            elif action.split()[0] == 'translate':
                self.parse_many(action, self.transl, 'translate')
            elif action.split()[0] in ['center_view', 'add_label', 'remove_label',
                                       'add_distance', 'remove_distance']:
                raise RuntimeError("{} is an instantaneous action (i.e. doesn't last over finite time interval) and "
                                   "cannot be combined with finite-time ones".format(action.split()[0]))
            super().parse(action, tuple(igns))
        self.action_type = [action.split()[0] for action in actions]
        if 'zoom_in' in self.action_type and 'zoom_out' in self.action_type:
            raise RuntimeError("Actions {} are mutually exclusive".format(", ".join(self.action_type)))
        if 't' not in self.parameters:
            raise RuntimeError("You can only combine finite-time actions using curly brackets. In directive "
                               "\n\n\t{}\n\n the duration is not specified; either rewrite it as consecutive "
                               "instantaneous actions, or add the 't=...s' parameter to one of them".format(command))
    
    def parse_many(self, directive, actions_dict, keyword):
        """
        Several types of actions have non-unique
        keywords or can be defined multiple times
        per Action, and hence are specifically handled
        by this function to put the params into
        a separate dictionary (e.g. self.highlights)
        :param directive: str, input section that defines a single Action in SimultaneousAction
        :param actions_dict: dict, the dictionary to handle the given action
        :param keyword: str, unique name of the action (e.g. 'highlight1')
        :return: None
        """
        actions_count = self.scene.counters[keyword]
        self.scene.counters[keyword] += 1
        spl = self.split_input_line(directive)
        try:
            prm_dict = {prm.split('=')[0]: '='.join(prm.split('=')[1:]).strip("'\"") for prm in spl[1:]}
        except IndexError:
            raise RuntimeError("Line '{}' is not formatted properly; action name should be followed by keyword=value "
                               "pairs, and no spaces should encircle the '=' sign".format(directive))
        if 'alias' in prm_dict.keys():
            alias = '_' + prm_dict['alias']
        elif keyword in ['translate', 'zoom']:
            alias = ''
        else:
            alias = str(actions_count)
        actions_dict[keyword + alias] = prm_dict
    

#if __name__ == "__main__":
def molywood():
    try:
        input_name = sys.argv[1]
    except IndexError:
        print("To run Molywood, provide the name of the text input file, e.g. "
              "'python path/to/moly.py script.txt'. To see and try out example "
              "input files, go to the 'examples' directory.")
        sys.exit(1)
    else:
        scr = Script(input_name)
        if len(sys.argv) == 2:
            scr.render()
        else:
            test_param = sys.argv[2]
            if test_param == '-test':
                for sscene in scr.scenes:
                    stcl_script = sscene.tcl()
                    if sscene.run_vmd:
                        with open('script_{}.tcl'.format(sscene.alias), 'w') as sout:
                            sout.write(stcl_script)
            else:
                print("\n\nWarning: parameters beyond the first will be ignored\n\n")
                scr.render()
