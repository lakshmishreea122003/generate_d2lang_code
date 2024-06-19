import os
import yaml
import csv
import google.generativeai as genai

class Diagrams:
    def __init__(self):
        self.c_string = ""

    @staticmethod
    def get_data():
        with open(r"D:\h1\d2lang\data.yaml", "r") as file:
            data = yaml.safe_load(file)
        return data
    
    def code(self):
        data = self.get_data()

        self.c_string += "# instances\n"
        for instance_name, instance_details in data['data']['instances'].items():
            details = ""
            if 'type' in instance_details:
                details += f"\\n{instance_details['type']}"
            if 'size' in instance_details:
                details += f"\\n{instance_details['size']}"
            self.c_string += f"{instance_name}: {instance_name}{details}\\n\n"

        self.c_string += "# connections\n"
        for connection in data['data']['connections']:
            self.c_string += f'{connection["from_instance"]}->{connection["to_instance"]}\n'
        
        return self.c_string 
    
    @staticmethod
    def gemini_architecture():
        genai.configure(api_key=os.environ.get('gemini_api'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "give example of a aws cloud architecture. Here mention names of each of the instances in standard short forms mention how many of these instances and also how each instance is connected to others. Give a paragraph. give unique responces everytime.  "
        res = model.generate_content(prompt)
        return res.text

    def gemini_yaml(self):
        genai.configure(api_key=os.environ.get('gemini_api'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        architecture = self.gemini_architecture()
        print(architecture)
        prompt = architecture + """ From this data I want to create a YAML file. In the YAML file. here data shoud be like data: instances: instance_name: type: type_of_instance . the format of the data should be like 
        data:
          instances:
            instance_name:
              type: type_of_instance
          connections:
            - from_instance: name
              to_instance: name
        if there are multiple instances with the same name, name them as instance_name-number: type: type_of_instance(it is a 2-3 words about the instance) . For example, instances: EC2-1, EC2-2, etc. Connections should be formatted as follows: connections: - from_instance: to_instance. there shoud be just instances and connections no other words to be used.  Generate the YAML data as instructed. no explaination required"""
        res = model.generate_content(prompt).text
        print(res)
        self.clean_and_save_yaml(res, "D:/h1/d2lang/data.yaml")
        return architecture

    @staticmethod
    def clean_and_save_yaml(data_string, output_filename):
        cleaned_data = data_string.replace("```yaml", "").replace("```", "").strip()
        data = yaml.safe_load(cleaned_data)
        with open(output_filename, "w") as file:
            yaml.dump(data, file, default_flow_style=False)
    
    def csv(self, arc, code):
        file_path = "C:/Users/Lakshmi/Downloads/d2lang_data.csv"
        file_exists = os.path.isfile(file_path)
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['architecture', 'code'])
            writer.writerow([arc, code])
        print("Data has been written")


    def execute(self):
        for i in range(5):
            arc = self.gemini_yaml()
            code = self.code()
            self.csv(arc,code)
            print(code)
            print(i)
        print("completed")

obj = Diagrams()
obj.execute()
# print(res)


