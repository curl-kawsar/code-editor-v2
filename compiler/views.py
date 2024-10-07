from rest_framework import viewsets
from rest_framework.response import Response
from .models import CodeSnippet
from .serializers import CodeSnippetSerializer
import subprocess
import tempfile
import os

class CodeSnippetViewSet(viewsets.ModelViewSet):
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSnippetSerializer

    def create(self, request, *args, **kwargs):
        code = request.data.get('code')
        input_data = request.data.get('input', [])
        lang = request.data.get('lang')
        result = self.execute_code(code, input_data, lang)
        snippet = CodeSnippet.objects.create(code=code, result=result)
        serializer = self.get_serializer(snippet)
        return Response(serializer.data)

    def execute_code(self, code, input_data, lang):
        temp_file_path = None
        try:
            if lang == "Python":
                command = ['python', '-c', code]
            elif lang == "JavaScript":
                command = ['node', '-e', code]
            elif lang == "Cpp":
                with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as temp_file:
                    temp_file.write(code.encode())
                    temp_file_path = temp_file.name
                compile_command = ['g++', temp_file_path, '-o', temp_file_path + '.out']
                compile_process = subprocess.run(compile_command, capture_output=True, text=True)
                if compile_process.returncode != 0:
                    return f"Compilation failed: {compile_process.stderr}"
                command = [temp_file_path + '.out']
            elif lang == "C":
                with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as temp_file:
                    temp_file.write(code.encode())
                    temp_file_path = temp_file.name
                compile_command = ['gcc', temp_file_path, '-o', temp_file_path + '.out']
                compile_process = subprocess.run(compile_command, capture_output=True, text=True)
                if compile_process.returncode != 0:
                    return f"Compilation failed: {compile_process.stderr}"
                command = [temp_file_path + '.out']
            elif lang == "Java":
                with tempfile.NamedTemporaryFile(suffix=".java", delete=False) as temp_file:
                    temp_file.write(code.encode())
                    temp_file_path = temp_file.name
                compile_command = ['javac', temp_file_path]
                compile_process = subprocess.run(compile_command, capture_output=True, text=True)
                if compile_process.returncode != 0:
                    return f"Compilation failed: {compile_process.stderr}"
                class_file_path = temp_file_path.replace(".java", "")
                command = ['java', '-cp', os.path.dirname(class_file_path), os.path.basename(class_file_path)]
            else:
                return "Unsupported language"

            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input='\n'.join(input_data), timeout=5)
            return stdout or stderr
        except subprocess.TimeoutExpired:
            return "Execution timed out"
        except subprocess.CalledProcessError as e:
            return f"Compilation failed: {e}"
        except FileNotFoundError as e:
            return f"Compiler not found: {e}"
        finally:
            if temp_file_path and lang in ["Cpp", "C", "Java"]:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                if lang in ["Cpp", "C"] and os.path.exists(temp_file_path + '.out'):
                    os.remove(temp_file_path + '.out')
                if lang == "Java":
                    class_file_path = temp_file_path.replace(".java", ".class")
                    if os.path.exists(class_file_path):
                        os.remove(class_file_path)

from django.shortcuts import render

def index(request):
    return render(request, 'compiler/index.html')