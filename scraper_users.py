from playwright.sync_api import sync_playwright
import json
import time
import random
from datetime import datetime

PERFILES = ["leaveerickalone", "juangabrielnarvaez"] # usuarios que se va a scrapear.



def auditoria_por_lotes(usernames):
    print(f"[*] Iniciando misión en bloque para {len(usernames)} cuentas...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("[*] Abriendo Instagram. Por favor, INICIA SESIÓN UNA VEZ.")
            page.goto("https://www.instagram.com/")

            page.wait_for_selector("svg[aria-label='Search'], svg[aria-label='Inicio']", timeout=60000)
            print("[*] ¡Sesión detectada! El bot toma el control...")

            for index, username in enumerate(usernames):
                print(f"\n[{index + 1}/{len(usernames)}] 🥷 Analizando a: @{username}")

                page.goto(f"https://www.instagram.com/{username}/")
                time.sleep(5)  # Tiempo para cargar el perfil

                script_js_base = f"""
                    async () => {{
                        try {{
                            const resProfile = await fetch('/api/v1/users/web_profile_info/?username={username}', {{
                                headers: {{ 'X-IG-App-ID': '936619743392459', 'X-Requested-With': 'XMLHttpRequest' }}
                            }});
                            const profileData = await resProfile.json();
                            const user = profileData.data.user;

                            const resFeed = await fetch('/api/v1/feed/user/{username}/username/', {{
                                headers: {{ 'X-IG-App-ID': '936619743392459', 'X-Requested-With': 'XMLHttpRequest' }}
                            }});
                            const feedData = await resFeed.json();

                            return {{
                                "perfil": {{
                                    "nombre": user.full_name,
                                    "biografia": user.biography,
                                    "seguidores": user.edge_followed_by.count,
                                    "seguidos": user.edge_follow.count,
                                    "total_posts": user.edge_owner_to_timeline_media.count
                                }},
                                "items": feedData.items
                            }};
                        }} catch (e) {{
                            return {{"error": e.toString()}};
                        }}
                    }}
                """

                datos_raw = page.evaluate(script_js_base)

                if "error" in datos_raw:
                    print(f"[!] Saltando @{username} por error de API: {datos_raw['error']}")
                    continue  # Salta a la siguiente cuenta de la lista

                perfil = datos_raw["perfil"]
                items = datos_raw["items"] or []

                resultado = {
                    "usuario": username,
                    "nombre": perfil["nombre"],
                    "seguidores": perfil["seguidores"],
                    "fecha_extraccion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "analisis_detallado": []
                }

                print(f"    - Extrayendo comentarios de sus publicaciones...")

                for item in items:
                    post_id = item.get('pk') or item.get('id')
                    shortcode = item.get('code')
                    likes = item.get('like_count', 0)
                    total_c = item.get('comment_count', 0)

                    script_comentarios = f"""
                        async () => {{
                            try {{
                                const res = await fetch('/api/v1/media/{post_id}/comments/', {{
                                    headers: {{ 'X-IG-App-ID': '936619743392459', 'X-Requested-With': 'XMLHttpRequest' }}
                                }});
                                return await res.json();
                            }} catch(e) {{ return null; }}
                        }}
                    """

                    datos_comentarios = page.evaluate(script_comentarios)
                    comentarios_formateados = []

                    if datos_comentarios and "comments" in datos_comentarios:
                        for c in datos_comentarios["comments"]:
                            comentarios_formateados.append({
                                "usuario": c.get('user', {}).get('username'),
                                "texto": c.get('text')
                            })

                    time.sleep(1)  # Pausa rápida entre fotos

                    tasa = 0
                    if perfil["seguidores"] > 0:
                        tasa = round(((likes + total_c) / perfil["seguidores"]) * 100, 2)

                    resultado["analisis_detallado"].append({
                        "post_id": shortcode,
                        "likes": likes,
                        "total_comentarios": total_c,
                        "tasa_interaccion_%": tasa,
                        "contenido_comentarios": comentarios_formateados
                    })

                # Guardamos el archivo individual de esta cuenta
                nombre_archivo = f"estudio_{username}.json"
                with open(nombre_archivo, 'w', encoding='utf-8') as f:
                    json.dump(resultado, f, ensure_ascii=False, indent=4)
                print(f"    ✅ Guardado: {nombre_archivo}")

                if index < len(usernames) - 1:
                    pausa = random.randint(12, 25)
                    print(f"    ⏳ Pausa táctica de {pausa} segundos para parecer humano...")
                    time.sleep(pausa)

            print("\n" + "=" * 50)
            print(" 🎉 ¡PROCESAMIENTO POR LOTES FINALIZADO! 🎉")
            print("=" * 50)

            print("\n🟢 Navegador libre. Presiona ENTER en la terminal para cerrar.")
            input("")
            browser.close()

        except Exception as e:
            print(f"[!] Error crítico en el bucle: {e}")
            browser.close()


auditoria_por_lotes(PERFILES)