import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

class FileService:
    """Serviço para gerenciamento de arquivos"""
    
    @staticmethod
    def allowed_file(filename):
        """Verifica se a extensão do arquivo é permitida"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    
    @staticmethod
    def save_uploaded_file(file, folder=''):
        """Salva um arquivo enviado e retorna o caminho"""
        if file and FileService.allowed_file(file.filename):
            # Gerar nome único para o arquivo
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Criar pasta se não existir
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
            os.makedirs(upload_path, exist_ok=True)
            
            # Salvar arquivo
            file_path = os.path.join(upload_path, unique_filename)
            file.save(file_path)
            
            # Retornar caminho relativo para o banco de dados
            return f"/static/uploads/{folder}/{unique_filename}"
        return None
    
    @staticmethod
    def delete_uploaded_file(file_path):
        """Deleta um arquivo enviado"""
        if file_path and not file_path.startswith('http'):
            try:
                # Remover /static/ do início se existir
                if file_path.startswith('/static/'):
                    file_path = file_path[8:]  # Remove '/static/'
                
                full_path = os.path.join('static', file_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
                    return True
            except Exception as e:
                current_app.logger.error(f"Erro ao deletar arquivo {file_path}: {e}")
        return False
    
    @staticmethod
    def get_file_size(file_path):
        """Retorna o tamanho do arquivo em bytes"""
        try:
            if file_path.startswith('/static/'):
                file_path = file_path[8:]
            full_path = os.path.join('static', file_path)
            if os.path.exists(full_path):
                return os.path.getsize(full_path)
        except Exception as e:
            current_app.logger.error(f"Erro ao obter tamanho do arquivo {file_path}: {e}")
        return 0
    
    @staticmethod
    def cleanup_orphaned_files():
        """Remove arquivos órfãos (não referenciados no banco)"""
        # Implementar lógica para limpar arquivos não utilizados
        pass 