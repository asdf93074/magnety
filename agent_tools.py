import os

def list_files():
    return os.listdir()

def read_file(filename: str):
    with open(filename, 'r') as f:
        return f.readlines()

def read_file_at_line(filename: str, line_number: int):
    with open(filename, 'r') as f:
        lines = f.readlines()
        return lines[line_number] 
    
def edit_line(filename: str, line_number: int, new_content: str, operation:   
 str = 'replace'):                                                             
     with open(filename) as f: lines = f.readlines()                           
     max_line = len(lines)                                                     
                                                                               
     # Replace operation: works on 1-based index                               
     if operation == 'replace':                                                
         if line_number < 1 or line_number > max_line:                         
             raise ValueError(f"Line {line_number} (1-based) in {filename} is invalid")                                                                     
         target_index = line_number - 1  # Convert to 0-based index            
         # Ensure proper newline handling                                      
         if new_content[-1:] != '\n': new_content += '\n'                      
         lines[target_index] = new_content                                     
                                                                               
     # Insert_after operation: inserts after specified line                    
     elif operation == 'insert_after':                                         
         if line_number < 1 or line_number + 1 > max_line + 1:                 
             raise ValueError(f"Insert after {line_number} in {filename} is invalid")                                                                     
                                                                               
         # Auto-append if line_number matches last line                        
         insert_pos = line_number if line_number < max_line else max_line      
         # Insert at next position (0-based)                                   
         lines.insert(insert_pos, new_content)                                 
                                                                               
     else: raise ValueError("Unsupported operation")                           
                                                                               
     with open(filename, 'w') as f:                                            
         f.writelines(lines)                                                   
                                                                               
     return f"{operation.replace('_', ' ').title()} at line {line_number} in {filename}"

tool_defs = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists all the files in the current directory.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads a file with the path name relative to current dir.",
            "parameters": { 
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to the file that you wish to read."
                    },
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file_at_line",
            "description": "Reads a file with the path name relative to current dir, but only at the specified line number. Always use this first to confirm the line number of a particular piece of code before replacing it.",
            "parameters": { 
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to the file that you wish to read."
                    },
                    "line_number": {
                        "type": "integer",
                        "description": "Line number to read from the file, starting from 0 and only a positive number."
                    },
                },
                "required": ["filename", "line_number"],
            },
        },
    },
    {                                                                             
         "type": "function",                                                       
         "function": {                                                             
             "description": "Edits specific lines in files by number (1-based)",   
             "name": "edit_line",                                                  
             "parameters": {                                                       
                 "type": "object",                                                 
                 "properties": {                                                   
                     "filename": {"type": "string"},                               
                     "line_number": {"type": "integer"},                           
                     "new_content": {"type": "string"},                            
                     "operation": {"type": "string", "enum": ["replace",           
     "insert_after"]}                                                              
                 },                                                                
                 "required": ["filename", "line_number", "new_content",            
     "operation"]                                                                  
             },                                                                    
             "strict": False                                                       
         }                                                                         
     }
]

tool_funcs = {
    "list_files": list_files,
    "read_file": read_file,
    "edit_line": edit_line,
    "read_file_at_line": read_file_at_line
}
