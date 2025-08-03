import streamlit as st
import json
import os

# Data persistence functions
def load_data():
    """Load data from JSON file if it exists"""
    data_file = "prompt_generator_data.json"
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return None

def save_data():
    """Save current session state to JSON file"""
    data_file = "prompt_generator_data.json"
    try:
        data = {
            'characters': st.session_state.characters,
            'poses': st.session_state.poses,
            'color_palettes': st.session_state.color_palettes,
            'art_styles': st.session_state.art_styles,
            'lighting_types': st.session_state.lighting_types,
            'backgrounds': st.session_state.backgrounds,
            'moods': st.session_state.moods,
            'expressions': st.session_state.expressions
        }
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# Load existing data or use defaults
saved_data = load_data()

# Initialize session state
# Initialize session state
if 'characters' not in st.session_state:
    if saved_data and 'characters' in saved_data:
        st.session_state.characters = saved_data['characters']
    else:
        st.session_state.characters = {
            "cyberpunk hacker girl": "neon-lit server room",
            "futuristic samurai": "cyberpunk Neo-Tokyo", 
            "anime spellcaster": "digital magic realm",
            "superhero": "cyberpunk metropolis"
        }

if 'poses' not in st.session_state:
    if saved_data and 'poses' in saved_data:
        st.session_state.poses = saved_data['poses']
    else:
        st.session_state.poses = [
            "dynamic crouched pose ready to strike with glowing weapon",
            "heroic standing pose with cape flowing in neon wind",
            "profile view looking upward thoughtfully with glowing eyes", 
            "arms outstretched with energy coursing through body",
            "confident standing with arms crossed and electric aura",
            "mid-air jumping pose with trailing energy effects",
            "sitting meditation pose with floating energy orbs",
            "walking forward with determination and glowing footsteps",
            "dramatic pose with one hand extended casting energy",
            "battle-ready stance with dual weapons glowing"
        ]

if 'color_palettes' not in st.session_state:
    if saved_data and 'color_palettes' in saved_data:
        st.session_state.color_palettes = saved_data['color_palettes']
    else:
        st.session_state.color_palettes = {
            "Cyberpunk Classic": "electric blue, hot pink, neon purple, cyan",
            "Neon Sunset": "neon orange, electric pink, bright purple, yellow glow",
            "Ice Fire": "ice blue, neon red, white, cyan",
            "Toxic Glow": "neon green, electric purple, bright cyan, lime"
        }

if 'art_styles' not in st.session_state:
    if saved_data and 'art_styles' in saved_data:
        st.session_state.art_styles = saved_data['art_styles']
    else:
        st.session_state.art_styles = [
            "anime style digital art",
            "highly detailed anime illustration", 
            "cyberpunk anime art style",
            "cinematic anime style digital art",
            "masterpiece anime artwork"
        ]

if 'lighting_types' not in st.session_state:
    if saved_data and 'lighting_types' in saved_data:
        st.session_state.lighting_types = saved_data['lighting_types']
    else:
        st.session_state.lighting_types = [
            "dramatic neon lighting",
            "cinematic rim lighting",
            "atmospheric neon glow",
            "multiple colored light sources",
            "volumetric neon lighting"
        ]

if 'backgrounds' not in st.session_state:
    if saved_data and 'backgrounds' in saved_data:
        st.session_state.backgrounds = saved_data['backgrounds']
    else:
        st.session_state.backgrounds = [
            "pure black background",
            "dark void with neon grid",
            "black background with subtle geometric patterns",
            "deep space black",
            "minimalist dark cityscape silhouette"
        ]

if 'moods' not in st.session_state:
    if saved_data and 'moods' in saved_data:
        st.session_state.moods = saved_data['moods']
    else:
        st.session_state.moods = [
            "dark and mysterious",
            "vibrant and energetic", 
            "serene and mystical",
            "intense and dramatic",
            "futuristic and clean"
        ]

if 'expressions' not in st.session_state:
    if saved_data and 'expressions' in saved_data:
        st.session_state.expressions = saved_data['expressions']
    else:
        st.session_state.expressions = [
            "confident and determined",
            "mysterious and enigmatic",
            "fierce and powerful",
            "calm and contemplative",
            "rebellious and edgy"
        ]

def add_character():
    """Basit öğe ekleme fonksiyonu"""
    st.header("➕ Yeni Öğe Ekle")
    
    # Tek satırda hızlı ekleme
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🎭 Karakter", "🤸 Pose", "🎨 Renk", "🎬 Art Style", "💡 Lighting", "🖼️ Background", "😊 Mood/Expression"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            char_name = st.text_input("Karakter:", placeholder="neon ninja")
            char_origin = st.text_input("Origin:", placeholder="futuristic dojo")
        with col2:
            if st.button("Ekle", key="char_add", use_container_width=True):
                if char_name and char_origin:
                    st.session_state.characters[char_name] = char_origin
                    save_data()  # Save to file
                    st.success("✅ Eklendi!")
                    st.rerun()
    
    with tab2:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_pose = st.text_input("Pose:", placeholder="flying through air with energy wings")
        with col2:
            if st.button("Ekle", key="pose_add", use_container_width=True):
                if new_pose:
                    st.session_state.poses.append(new_pose)
                    save_data()  # Save to file
                    st.success("✅ Eklendi!")
                    st.rerun()
    
    with tab3:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            palette_name = st.text_input("Palet Adı:", placeholder="Rainbow Neon")
        with col2:
            palette_colors = st.text_input("Renkler:", placeholder="rainbow colors, multi-spectrum glow")
        with col3:
            if st.button("Ekle", key="palette_add", use_container_width=True):
                if palette_name and palette_colors:
                    st.session_state.color_palettes[palette_name] = palette_colors
                    save_data()  # Save to file
                    st.success("✅ Eklendi!")
                    st.rerun()
    
    with tab4:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_art_style = st.text_input("Art Style:", placeholder="hyper-realistic anime digital painting")
        with col2:
            if st.button("Ekle", key="art_add", use_container_width=True):
                if new_art_style:
                    st.session_state.art_styles.append(new_art_style)
                    save_data()  # Save to file
                    st.success("✅ Eklendi!")
                    st.rerun()
    
    with tab5:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_lighting = st.text_input("Lighting:", placeholder="holographic rainbow lighting with prism effects")
        with col2:
            if st.button("Ekle", key="light_add", use_container_width=True):
                if new_lighting:
                    st.session_state.lighting_types.append(new_lighting)
                    save_data()  # Save to file
                    st.success("✅ Eklendi!")
                    st.rerun()
    
    with tab6:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_background = st.text_input("Background:", placeholder="floating digital matrix void")
        with col2:
            if st.button("Ekle", key="bg_add", use_container_width=True):
                if new_background:
                    st.session_state.backgrounds.append(new_background)
                    save_data()  # Save to file
                    st.success("✅ Eklendi!")
                    st.rerun()
    
    with tab7:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            new_mood = st.text_input("Mood:", placeholder="epic and heroic")
        with col2:
            new_expression = st.text_input("Expression:", placeholder="wise and ancient")
        with col3:
            if st.button("Ekle", key="mood_add", use_container_width=True):
                if new_mood:
                    st.session_state.moods.append(new_mood)
                if new_expression:
                    st.session_state.expressions.append(new_expression)
                if new_mood or new_expression:
                    save_data()  # Save to file
                    st.success("✅ Eklendi!")
                    st.rerun()

def generate_prompt():
    """Prompt oluşturma fonksiyonu"""
    st.header("🚀 Prompt Oluştur")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_char = st.selectbox("Karakter Seç:", list(st.session_state.characters.keys()))
        selected_pose = st.selectbox("Pose Seç:", st.session_state.poses)
    
    with col2:
        selected_palette = st.selectbox("Renk Paleti Seç:", list(st.session_state.color_palettes.keys()))
        
        # Gelişmiş ayarlar
        art_style = st.selectbox("Art Style:", st.session_state.art_styles)
        
    with col3:
        lighting_type = st.selectbox("Lighting:", st.session_state.lighting_types)
        
        background_type = st.selectbox("Background:", st.session_state.backgrounds)
        
    # Gelişmiş seçenekler
    with st.expander("🎛️ Gelişmiş Ayarlar"):
        col4, col5 = st.columns(2)
        
        with col4:
            quality_level = st.selectbox("Kalite:", [
                "masterpiece, best quality, ultra detailed",
                "8K ultra HD, professional artwork",
                "award-winning digital art, perfect composition",
                "studio quality, photorealistic rendering"
            ])
            
            effects = st.multiselect("Görsel Efektler:", [
                "soft outer glow",
                "volumetric lighting",
                "particle effects", 
                "energy aura",
                "holographic elements",
                "light bloom and lens flare",
                "electromagnetic field visualization"
            ], default=["soft outer glow", "volumetric lighting"])
            
        with col5:
            mood = st.selectbox("Atmosfer:", st.session_state.moods)
            
            expression = st.selectbox("İfade:", st.session_state.expressions)
        
    if st.button("🎨 ULTRA PROMPT OLUŞTUR", type="primary", use_container_width=True):
        origin = st.session_state.characters[selected_char]
        colors = st.session_state.color_palettes[selected_palette]
        effects_str = ", ".join(effects) if effects else "soft outer glow"
        
        # Mega detaylı prompt oluştur
        detailed_prompt = f"{quality_level}, {art_style}, {selected_char} from {origin}, {expression} expression, {selected_pose}, wearing detailed outfit with intricate design elements, {lighting_type} with strong rim lighting creating dramatic shadows, {background_type}, {colors} with glowing edges and neon accents, {effects_str}, {mood} atmosphere, sharp focus, perfect composition, cinematic quality"
        
        # Ultra detaylı JSON
        prompt_data = {
            "metadata": {
                "generator": "Neon Anime Prompt Generator v2.0",
                "timestamp": st.session_state.get('timestamp', '2024-08-03'),
                "version": "professional",
                "style_category": "cyberpunk_neon_anime"
            },
            "character_details": {
                "character_name": selected_char,
                "origin_world": origin,
                "personality": expression,
                "visual_description": f"{expression} {selected_char} with intricate design details"
            },
            "visual_composition": {
                "art_style": art_style,
                "pose_description": selected_pose,
                "lighting_system": lighting_type,
                "background_setting": background_type,
                "atmosphere": mood
            },
            "color_system": {
                "palette_name": selected_palette,
                "color_scheme": colors,
                "glow_effects": "neon edges with luminescent outlines",
                "contrast": "high contrast with vibrant saturation"
            },
            "technical_specifications": {
                "quality_level": quality_level,
                "visual_effects": effects,
                "rendering_style": "photorealistic with anime aesthetics",
                "resolution": "8K ultra HD",
                "lighting_model": "ray-traced with volumetric rendering"
            },
            "dall_e_optimized_prompt": detailed_prompt,
            "alternative_prompts": {
                "short_version": f"{art_style}, {selected_char}, {selected_pose}, {colors}, {background_type}",
                "midjourney_style": f"{selected_char} from {origin} :: {selected_pose} :: {colors} :: {lighting_type} :: anime style --ar 16:9 --niji",
                "stable_diffusion": f"({quality_level}), {art_style}, {selected_char}, {origin}, {selected_pose}, {colors}, {lighting_type}, {background_type}"
            },
            "style_tags": [
                "cyberpunk", "neon", "anime", "digital_art", "futuristic", 
                "glowing_effects", "dramatic_lighting", "high_contrast", "professional_quality"
            ],
            "prompt_engineering_notes": {
                "strength_keywords": ["masterpiece", "ultra detailed", "professional", "cinematic"],
                "color_emphasis": "neon glow effects prioritized",
                "composition_focus": "character-centered with dramatic lighting",
                "style_consistency": "maintained anime aesthetic with cyberpunk elements"
            }
        }
        
        st.success("✅ Ultra Detaylı Prompt Oluşturuldu!")
        
        # Sonuçları göster
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Ana Prompt", "📋 Detaylı JSON", "🔄 Alternatifler", "📊 Analiz"])
        
        with tab1:
            st.subheader("🎨 DALL-E için Optimize Edilmiş Prompt:")
            st.code(detailed_prompt, language=None)
            
        with tab2:
            st.subheader("📋 Profesyonel JSON Çıktısı:")
            st.json(prompt_data)
            
        with tab3:
            st.subheader("🔄 Diğer AI Platformları için Alternatifler:")
            st.write("**Kısa Versiyon:**")
            st.code(prompt_data["alternative_prompts"]["short_version"])
            st.write("**Midjourney Tarzı:**")
            st.code(prompt_data["alternative_prompts"]["midjourney_style"])
            st.write("**Stable Diffusion:**")
            st.code(prompt_data["alternative_prompts"]["stable_diffusion"])
            
        with tab4:
            st.subheader("📊 Prompt Analizi:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Toplam Kelime", len(detailed_prompt.split()))
                st.metric("Stil Tagları", len(prompt_data["style_tags"]))
                st.metric("Efekt Sayısı", len(effects))
            with col_b:
                st.write("**Güçlü Kelimeler:**")
                for word in prompt_data["prompt_engineering_notes"]["strength_keywords"]:
                    st.write(f"• {word}")
        
        return prompt_data

# Ana uygulama
def main():
    st.set_page_config(page_title="Neon Anime Generator", page_icon="⚡", layout="wide")
    
    st.title("⚡ Neon Anime Prompt Generator")
    st.markdown("---")
    
    # Sidebar menü
    with st.sidebar:
        st.header("🎛️ Menü")
        mode = st.radio("Mod Seç:", ["🎨 Prompt Oluştur", "➕ Öğe Ekle"])
    
    if mode == "➕ Öğe Ekle":
        add_character()
    else:
        generate_prompt()
    
    # Mevcut öğeleri göster
    with st.sidebar:
        st.markdown("---")
        st.subheader("📊 Mevcut Öğeler")
        st.write(f"🎭 Karakterler: {len(st.session_state.characters)}")
        st.write(f"🤸 Pozlar: {len(st.session_state.poses)}")
        st.write(f"🎨 Paletler: {len(st.session_state.color_palettes)}")
        st.write(f"🎬 Art Styles: {len(st.session_state.art_styles)}")
        st.write(f"💡 Lighting: {len(st.session_state.lighting_types)}")
        st.write(f"🖼️ Backgrounds: {len(st.session_state.backgrounds)}")
        st.write(f"😊 Moods: {len(st.session_state.moods)}")
        st.write(f"😎 Expressions: {len(st.session_state.expressions)}")
        
        # Data management
        st.markdown("---")
        st.subheader("💾 Veri Yönetimi")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Kaydet", use_container_width=True):
                if save_data():
                    st.success("✅ Veriler kaydedildi!")
                else:
                    st.error("❌ Kayıt başarısız!")
        
        with col2:
            if st.button("🔄 Yenile", use_container_width=True):
                st.rerun()
        
        # Persistent storage info
        st.info("ℹ️ Eklediğiniz öğeler otomatik olarak kaydedilir ve sayfa yenilendiğinde korunur.")
        
        # Detayları göster
        if st.checkbox("Detayları Göster"):
            st.write("**Karakterler:**")
            for char, origin in st.session_state.characters.items():
                st.write(f"• {char} → {origin}")

if __name__ == "__main__":
    main()