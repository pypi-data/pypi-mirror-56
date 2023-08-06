# Import statements
import os
import stat
import shutil
import importlib
import importlib.util

import jinja2


class Template(object):
    
    BOILERPLATE_MARKER_START = '"""<<<\n'
    BOILERPLATE_MARKER_END = '>>>"""\n'
    SUMMARISE_FILE_NAME = 'all.sh'
    
    def __init__(self, path, boilerplate_path=None):
        self.path = path
        self.boilerplate_path = boilerplate_path
        self.render_me = self._load_render_me()
        self.boilerplate_str = self._load_boilerplate_str()
        
    def _load_render_me(self):
        
        # Import the module
        spec = importlib.util.spec_from_file_location("renderModule",
                                                      self.path)
        renderModule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderModule)
        
        # Access the render() function
        render = renderModule.render

        # Return the render funtion
        return render
    
    def _load_boilerplate_str(self):
        if self.boilerplate_path:
            with open(self.boilerplate_path, 'r') as f:
                lines = f.readlines()
        else:
            with open(self.path, 'r') as f:
                lines = f.readlines()
            i_start = lines.index(self.BOILERPLATE_MARKER_START)
            i_end = lines.index(self.BOILERPLATE_MARKER_END)
            lines = lines[i_start+1 : i_end]
        return ''.join(lines) # Not '\n' because readlines() returns lines with added '\n'
        
    def create_files(self, outdir, start_command=None):
        """
        Set start_command to generate a summary file.
        """
        
        text_template = jinja2.Environment(loader=jinja2.BaseLoader).from_string(self.boilerplate_str)
        
        # Whipe out output dir and recreate
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        os.makedirs(outdir)
        
        # Render the template
        files = []
        for file_name, context in self.render_me():
            
            rendered_template = text_template.render(context)
            
            full_save_path = os.path.join(outdir, file_name)
            
            with open(full_save_path, "w") as f:
                f.write(rendered_template)
                
            files.append(os.path.abspath(full_save_path))
            
        # Write summary
        if start_command:
            
            # Build file list
            file_names = [os.path.basename(f) for f in files]
            
            # Write to file
            with open(os.path.join(outdir, self.SUMMARISE_FILE_NAME), "w") as f:
                for line in file_names:
                    f.writelines(start_command + ' ' + line + '\n')
                    
            # Make it executable
            st = os.stat(os.path.join(outdir, self.SUMMARISE_FILE_NAME))
            os.chmod(os.path.join(outdir, self.SUMMARISE_FILE_NAME), st.st_mode | stat.S_IEXEC)
            
            # Add to created files
            files.append(os.path.abspath(os.path.join(outdir, self.SUMMARISE_FILE_NAME)))
                
        # Return all the saved files
        return files
    
