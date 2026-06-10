"""
Video Assembler - Junta tudo em vídeo final
Usa: edge-tts (narração) + FFmpeg (edição)
"""
import asyncio
import json
import os
import subprocess
from pathlib import Path
import edge_tts

# Vozes disponíveis para PT-BR
VOZES_PTBR = {
    "francisca": "pt-BR-FranciscaNeural",
    "antonio": "pt-BR-AntonioNeural",
}

async def gerar_narracao(texto: str, voz: str, output_path: str) -> str:
    """Gera áudio de narração com edge-tts"""
    communicate = edge_tts.Communicate(texto, voz)
    await communicate.save(output_path)
    return output_path

async def gerar_narracao_com_srt(texto: str, voz: str, audio_path: str, srt_path: str) -> tuple:
    """Gera áudio + legenda SRT sincronizada"""
    communicate = edge_tts.Communicate(texto, voz)
    submaker = edge_tts.SubMaker()
    
    with open(audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    
    # Salva SRT
    srt_content = submaker.generate_subs()
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    return audio_path, srt_path

def get_audio_duration(audio_path: str) -> float:
    """Obtém duração do áudio em segundos"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def concat_videos(video_paths: list, output_path: str):
    """Concatena múltiplos vídeos"""
    # Cria arquivo de lista
    list_file = output_path + ".txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for vp in video_paths:
            f.write(f"file '{os.path.abspath(vp)}'\n")
    
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_file, "-c", "copy", output_path
    ], capture_output=True)
    
    os.remove(list_file)

def overlay_avatar(video_path: str, avatar_path: str, output_path: str,
                   position: str = "bottom-right", scale: float = 0.25):
    """Sobrepõe avatar no vídeo (picture-in-picture)"""
    # Posições
    positions = {
        "bottom-right": "W-w-20:H-h-20",
        "bottom-left": "20:H-h-20",
        "top-right": "W-w-20:20",
        "top-left": "20:20",
        "center": "(W-w)/2:(H-h)/2",
    }
    pos = positions.get(position, positions["bottom-right"])
    
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", avatar_path,
        "-filter_complex",
        f"[1:v]scale=iw*{scale}:ih*{scale}[avatar];[0:v][avatar]overlay={pos}",
        "-c:a", "copy",
        output_path
    ], capture_output=True)

def burn_subtitles(video_path: str, srt_path: str, output_path: str,
                   font_size: int = 24, font_color: str = "white"):
    """Queima legendas no vídeo"""
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}:force_style='FontSize={font_size},PrimaryColour=&H00FFFFFF'",
        "-c:a", "copy",
        output_path
    ], capture_output=True)

def add_audio_to_video(video_path: str, audio_path: str, output_path: str):
    """Adiciona áudio ao vídeo"""
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_path
    ], capture_output=True)

def resize_video(video_path: str, width: int, height: int, output_path: str):
    """Redimensiona vídeo mantendo aspect ratio"""
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        "-c:a", "copy",
        output_path
    ], capture_output=True)

async def assembler_aula(roteiro_path: str, output_dir: str, voz: str = "antonio"):
    """Monta aula completa: narração + vídeo + avatar + legendas"""
    
    # Carrega roteiro
    with open(roteiro_path, 'r', encoding='utf-8') as f:
        roteiro = json.load(f)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Diretórios
    audio_dir = output_path / "audio"
    srt_dir = output_path / "legendas"
    temp_dir = output_path / "temp"
    audio_dir.mkdir(exist_ok=True)
    srt_dir.mkdir(exist_ok=True)
    temp_dir.mkdir(exist_ok=True)
    
    print(f"🎬 Montando aula: {roteiro.get('projeto', 'Sem nome')}")
    print(f"   Voz: {voz}")
    print(f"   Cenas: {len(roteiro['cenas'])}")
    
    scene_videos = []
    
    for i, cena in enumerate(roteiro['cenas'], 1):
        print(f"\n   📝 Cena {i}/{len(roteiro['cenas'])}: {cena.get('descricao', '')[:50]}...")
        
        # 1. Gerar narração
        audio_file = str(audio_dir / f"scene_{i:03d}.mp3")
        srt_file = str(srt_dir / f"scene_{i:03d}.srt")
        
        narracao_text = cena.get('narracao', cena.get('dalle_prompt', ''))
        print(f"      🔊 Gerando narração...")
        await gerar_narracao_com_srt(narracao_text, voz, audio_file, srt_file)
        
        # 2. Verificar se vídeo da cena existe
        video_file = str(output_path.parent / "videos_hd" / f"scene_{i:03d}_hd.mp4")
        if not os.path.exists(video_file):
            video_file = str(output_path.parent / "videos" / f"scene_{i:03d}.mp4")
        
        if not os.path.exists(video_file):
            print(f"      ⚠️ Vídeo não encontrado: {video_file}")
            continue
        
        # 3. Adicionar narração ao vídeo
        video_with_audio = str(temp_dir / f"scene_{i:03d}_audio.mp4")
        print(f"      🎵 Adicionando narração...")
        add_audio_to_video(video_file, audio_file, video_with_audio)
        
        # 4. Queimar legendas
        video_with_subs = str(temp_dir / f"scene_{i:03d}_subs.mp4")
        print(f"      📝 Queimando legendas...")
        burn_subtitles(video_with_audio, srt_file, video_with_subs)
        
        scene_videos.append(video_with_subs)
    
    if not scene_videos:
        print("❌ Nenhum vídeo encontrado para montar!")
        return None
    
    # 5. Concatenar todas as cenas
    final_video = str(output_path / f"{roteiro.get('projeto', 'aula').replace(' ', '_')}_final.mp4")
    print(f"\n   🔗 Concatenando {len(scene_videos)} cenas...")
    concat_videos(scene_videos, final_video)
    
    # Limpeza
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print(f"\n✅ Vídeo final salvo em: {final_video}")
    return final_video

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python video_assembler.py <roteiro.json> [output_dir] [voz]")
        print("Vozes disponíveis: francisca, antonio")
        sys.exit(1)
    
    roteiro = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "./output_final"
    voz = sys.argv[3] if len(sys.argv) > 3 else "antonio"
    
    asyncio.run(assembler_aula(roteiro, output, voz))
