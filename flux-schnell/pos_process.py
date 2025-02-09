import os
import subprocess

def process_images_by_uuid(uuid_dir):
    """
    Processa todas as imagens dentro do diretório upscaly/uuid e salva em pos_process/uuid
    usando o comando ImageMagick diretamente.
    
    Args:
        uuid_dir (str): UUID do diretório a ser processado
    """
    # Definir os diretórios
    input_dir = os.path.join("./upscaly", uuid_dir)
    output_dir = os.path.join("./pos_process", uuid_dir)
    
    # Verificar se o diretório de entrada existe
    if not os.path.exists(input_dir):
        print(f"Diretório de entrada não encontrado: {input_dir}")
        return
    
    # Criar diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Construir o comando ImageMagick
        command = [
            "magick", "mogrify",
            "-sharpen", "0x1",
            "-contrast-stretch", "2%x98%",
            "-brightness-contrast", "-5x10",
            "-modulate", "95,105",
            "-colorize", "5,2,0",
            "-attenuate", "0.5",
            "+noise", "Gaussian",
            "-path", output_dir,
            os.path.join(input_dir, "*.png")
        ]
        
        # Executar o comando
        print("Executando comando ImageMagick...")
        print(f"Comando: {' '.join(command)}")
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        
        # Verificar se houve erro
        if result.returncode != 0:
            print(f"Erro ao processar imagens: {result.stderr}")
            return
        
        print("Processamento concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")

if __name__ == "__main__":
    # Exemplo de uso
    uuid = input("Digite o UUID do diretório a ser processado: ")
    process_images_by_uuid(uuid)
