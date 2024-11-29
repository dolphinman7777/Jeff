import os

def read_training_data():
    """Read all training data files"""
    data = {
        'philosophy': {},
        'technology': {},
        'creativity': {}
    }
    
    base_dir = "training_data"
    for category in data.keys():
        category_dir = os.path.join(base_dir, category)
        if os.path.exists(category_dir):
            for file in os.listdir(category_dir):
                if file.endswith('.txt'):
                    path = os.path.join(category_dir, file)
                    with open(path, 'r') as f:
                        data[category][file] = f.read()
    
    return data

def generate_modelfile():
    training_data = read_training_data()
    
    modelfile_content = 'FROM llama2\n'
    modelfile_content += 'SYSTEM "You are Jeff, an AI assistant trained on philosophy, technology, and creativity."\n\n'
    
    # Add training data as messages
    for category, files in training_data.items():
        for filename, content in files.items():
            # Escape quotes and clean content
            clean_content = content.replace('"', '\\"').replace('\n', ' ').strip()
            modelfile_content += f'MESSAGE "user" "Learn this {category} content from {filename}"\n'
            modelfile_content += f'MESSAGE "assistant" "I have learned the {category} concepts from {filename}"\n\n'
    
    modelfile_content += 'PARAMETER temperature 0.7\n'
    modelfile_content += 'PARAMETER top_p 0.9\n'
    
    with open("Modelfile", "w", newline='\n') as f:
        f.write(modelfile_content)

if __name__ == "__main__":
    generate_modelfile()
    print("Generated Modelfile successfully") 