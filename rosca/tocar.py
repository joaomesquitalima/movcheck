# audio_player.py
import pygame

def play_sound(file_path):
    """
    Reproduz um arquivo de som usando pygame.

    :param file_path: Caminho para o arquivo de áudio (ex: 'teste.mp3')
    """
    # Inicializa o mixer do pygame
    pygame.mixer.init()

    try:
        # Carrega o arquivo de áudio
        pygame.mixer.music.load(file_path)

        # Reproduz o arquivo de áudio
        pygame.mixer.music.play()

        # Mantém o script rodando enquanto a música está tocando
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Erro ao tentar reproduzir o som: {e}")
    finally:
        # Encerra o mixer do pygame após a reprodução
        pygame.mixer.quit()
