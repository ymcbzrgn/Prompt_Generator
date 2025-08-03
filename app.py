import streamlit as st
import json
import os
import requests
import time
import streamlit.components.v1 as components
from typing import Optional, Dict, Any

# Data persistence functions
def copy_to_clipboard(text, button_key):
    """JavaScript ile metni panoya kopyala"""
    # JavaScript escape edilmiş metin
    escaped_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('"', '\\"').replace("'", "\\'")
    copy_script = f"""
    <script>
    function copyText_{button_key}() {{
        const text = `{escaped_text}`;
        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(text).then(function() {{
                console.log('Text copied to clipboard successfully');
            }}).catch(function(err) {{
                console.error('Clipboard API failed: ', err);
                fallbackCopy(text);
            }});
        }} else {{
            fallbackCopy(text);
        }}
        
        function fallbackCopy(text) {{
            const textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.position = "fixed";
            textArea.style.left = "-999999px";
            textArea.style.top = "-999999px";
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {{
                document.execCommand('copy');
                console.log('Fallback copy successful');
            }} catch (err) {{
                console.error('Fallback copy failed: ', err);
            }}
            document.body.removeChild(textArea);
        }}
    }}
    copyText_{button_key}();
    </script>
    """
    components.html(copy_script, height=0)

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

# AI API Integration with Enhanced Caching
@st.cache_data(ttl=86400, show_spinner=False)  # Cache for 24 hours (more aggressive)
def get_cached_prompt_enhancement(base_prompt: str, style: str, character: str) -> Optional[str]:
    """Cached function to avoid repeated API calls for similar prompts"""
    # This function should actually perform the API call, not return None
    # Streamlit will handle the caching automatically
    return None  # This will be replaced by actual API call result

def call_gemini_api(prompt: str, api_key: str, creativity: float = 0.8, max_tokens: int = 200, 
                   focus: str = "Genel Artistik Kalite", model: str = "gemini-1.5-flash") -> Optional[str]:
    """Call AI API with error handling and customizable parameters"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        
        # Dynamic system prompt based on focus
        focus_prompts = {
            "Genel Artistik Kalite": "Focus on overall artistic quality, professional terminology, and visual impact",
            "Işık ve Atmosfer": "Focus on lighting effects, atmospheric elements, and mood enhancement",
            "Karakter Detayları": "Focus on character design, clothing details, and facial expressions",
            "Kompozisyon ve Açılar": "Focus on camera angles, composition, and visual perspective",
            "Malzeme ve Dokular": "Focus on materials, textures, surface details, and tactile qualities"
        }
        
        system_prompt = f"""You are an expert AI art prompt engineer specializing in anime and digital art. 

TASK: Enhance the given prompt to be more artistic and detailed while maintaining all core elements.

FOCUS: {focus_prompts.get(focus, focus_prompts["Genel Artistik Kalite"])}

ENHANCEMENT RULES:
- Keep ALL original characters, settings, colors, and key descriptors
- Add 5-10 high-impact artistic enhancement words/phrases
- Use professional photography and digital art terminology
- Enhance lighting, texture, and atmospheric details
- Make descriptions more specific and vivid
- Add technical quality indicators
- Maintain the cyberpunk/neon anime aesthetic
- DO NOT add explanations or meta-commentary
- Return ONLY the enhanced prompt

Original prompt to enhance:"""
        
        data = {
            "contents": [{
                "parts": [{
                    "text": f"{system_prompt}\n\n{prompt}"
                }]
            }],
            "generationConfig": {
                "temperature": creativity,
                "maxOutputTokens": max_tokens,
                "topP": min(0.95, creativity + 0.1),
                "topK": int(40 * creativity),
                "stopSequences": ["Original:", "Explanation:", "Note:", "Focus:", "Enhancement:"]
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            # Debug: Print the API response structure
            # st.write("Debug - API Response:", result)
            
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                
                # Check if candidate has content/parts structure
                if 'content' in candidate and 'parts' in candidate['content']:
                    enhanced_prompt = candidate['content']['parts'][0]['text'].strip()
                elif 'parts' in candidate:
                    enhanced_prompt = candidate['parts'][0]['text'].strip()
                else:
                    st.error(f"Unexpected API response structure: {candidate}")
                    return None
                
                # Clean up any unwanted text
                enhanced_prompt = enhanced_prompt.replace("Enhanced prompt:", "").strip()
                enhanced_prompt = enhanced_prompt.replace("Enhanced:", "").strip()
                return enhanced_prompt
            else:
                if 'error' in result:
                    st.error(f"API Error: {result['error']}")
                else:
                    st.error(f"No candidates in response: {result}")
        else:
            error_text = response.text
            st.warning(f"API Error {response.status_code}: {error_text}")
            
    except Exception as e:
        st.warning(f"API call failed: {str(e)}")
    
    return None

def enhance_prompt_with_gemini(base_prompt: str, character: str, style: str, 
                              creativity: float = 0.8, max_tokens: int = 200, 
                              focus: str = "Genel Artistik Kalite") -> tuple[str, dict]:
    """Enhance prompt using AI with fallback API keys and return debug info"""
    
    debug_info = {
        "api_used": None,
        "cache_hit": False,
        "original_length": len(base_prompt.split()),
        "enhanced_length": 0,
        "processing_time": 0,
        "settings": {
            "creativity": creativity,
            "max_tokens": max_tokens,
            "focus": focus
        }
    }
    
    start_time = time.time()
    
    # Check if API keys are configured
    api_key_1 = st.secrets.get("GEMINI_API_KEY_1", "")
    api_key_2 = st.secrets.get("GEMINI_API_KEY_2", "")
    
    if not api_key_1 and not api_key_2:
        debug_info["error"] = "No API keys configured"
        return base_prompt, debug_info
    
    # Create more efficient cache key (less specific = more cache hits)
    # Group similar prompts together by using normalized components
    cache_key = f"{hash(base_prompt[:100])}_{creativity:.1f}_{max_tokens//50}_{focus[:10]}_{character[:5]}_{style[:10]}"
    
    # Try to get cached result first with more aggressive caching
    try:
        # First try exact cache
        cached_result = cached_gemini_call(cache_key, base_prompt, api_key_1 or api_key_2, 
                                         creativity, max_tokens, focus)
        if cached_result and cached_result != base_prompt:
            debug_info["cache_hit"] = True
            debug_info["enhanced_length"] = len(cached_result.split())
            debug_info["processing_time"] = time.time() - start_time
            return cached_result, debug_info
        
        # Second try: similar prompt cache (more lenient)
        similar_cache_key = f"{hash(base_prompt[:50])}_{focus[:5]}_{character[:3]}"
        cached_result = cached_gemini_call(similar_cache_key, base_prompt, api_key_1 or api_key_2,
                                         creativity, max_tokens, focus)
        if cached_result and cached_result != base_prompt:
            debug_info["cache_hit"] = True
            debug_info["cache_type"] = "similar"
            debug_info["enhanced_length"] = len(cached_result.split())
            debug_info["processing_time"] = time.time() - start_time
            return cached_result, debug_info
            
    except:
        pass  # If cache fails, continue with API call
    
    # Try primary API key
    if api_key_1:
        enhanced = call_gemini_api(base_prompt, api_key_1, creativity, max_tokens, focus)
        if enhanced and enhanced != base_prompt:
            debug_info["api_used"] = "Primary"
            debug_info["enhanced_length"] = len(enhanced.split())
            debug_info["processing_time"] = time.time() - start_time
            return enhanced, debug_info
        time.sleep(1)  # Brief delay before fallback
    
    # Fallback to secondary API key
    if api_key_2:
        enhanced = call_gemini_api(base_prompt, api_key_2, creativity, max_tokens, focus)
        if enhanced and enhanced != base_prompt:
            debug_info["api_used"] = "Fallback"
            debug_info["enhanced_length"] = len(enhanced.split())
            debug_info["processing_time"] = time.time() - start_time
            return enhanced, debug_info
    
    # Return original if all API calls fail
    debug_info["error"] = "All API calls failed"
    debug_info["processing_time"] = time.time() - start_time
    return base_prompt, debug_info

# Enhanced cached function with longer TTL and better key strategy
@st.cache_data(ttl=86400, show_spinner=False)  # 24 hour cache
def cached_gemini_call(cache_key: str, base_prompt: str, api_key: str, 
                      creativity: float, max_tokens: int, focus: str) -> Optional[str]:
    """Cached version of AI API call with aggressive caching for token efficiency"""
    return call_gemini_api(base_prompt, api_key, creativity, max_tokens, focus)

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
            
    # AI Enhancement Toggle
    with st.expander("🤖 AI Enhancement"):
        col_ai_main1, col_ai_main2 = st.columns(2)
        
        with col_ai_main1:
            use_ai_enhancement = st.checkbox("✨ AI ile Prompt Geliştir", value=True, 
                                           help="AI ile prompt'u otomatik olarak geliştirir")
        
        with col_ai_main2:
            show_debug_info = st.checkbox("� Teknik Detaylar", value=False,
                                        help="Geliştiriciler için teknik bilgiler")
        
        if use_ai_enhancement:
            col_ai1, col_ai2 = st.columns(2)
            with col_ai1:
                st.info("🚀 AI kullanarak prompt'unuz daha detaylı ve artistik hale getirilecek")
            with col_ai2:
                st.info("💡 **AI işlem hızlandırma** - Son 24 saat içinde benzer prompt'lar için AI sonuçları hızlıca yüklenir.")
                
            # Advanced AI settings - Using columns instead of nested expander
            st.markdown("**⚙️ Gelişmiş AI Ayarları:**")
            col_set1, col_set2 = st.columns(2)
            with col_set1:
                ai_creativity = st.slider("Yaratıcılık Seviyesi", 0.1, 1.0, 0.8, 0.1,
                                        help="Düşük: Daha muhafazakar, Yüksek: Daha yaratıcı")
                max_tokens = st.slider("Maksimum Token", 100, 300, 200, 50,
                                     help="Daha uzun çıktı için artırın")
            with col_set2:
                enhancement_focus = st.selectbox("Geliştirme Odağı:", [
                    "Genel Artistik Kalite",
                    "Işık ve Atmosfer",
                    "Karakter Detayları",
                    "Kompozisyon ve Açılar",
                    "Malzeme ve Dokular"
                ])
        else:
            ai_creativity = 0.8
            max_tokens = 200
            enhancement_focus = "Genel Artistik Kalite"
            show_debug_info = False
    
    if st.button("🎨 ULTRA PROMPT OLUŞTUR", type="primary", use_container_width=True):
        origin = st.session_state.characters[selected_char]
        colors = st.session_state.color_palettes[selected_palette]
        effects_str = ", ".join(effects) if effects else "soft outer glow"
        
        # Base prompt oluştur
        base_prompt = f"{quality_level}, {art_style}, {selected_char} from {origin}, {expression} expression, {selected_pose}, wearing detailed outfit with intricate design elements, {lighting_type} with strong rim lighting creating dramatic shadows, {background_type}, {colors} with glowing edges and neon accents, {effects_str}, {mood} atmosphere, sharp focus, perfect composition, cinematic quality"
        
        # AI Enhancement
        debug_info = None
        if use_ai_enhancement:
            with st.spinner("🤖 AI ile prompt geliştiriliyor..."):
                enhanced_prompt, debug_info = enhance_prompt_with_gemini(
                    base_prompt, selected_char, art_style, 
                    ai_creativity, max_tokens, enhancement_focus
                )
                detailed_prompt = enhanced_prompt
                ai_enhanced = enhanced_prompt != base_prompt
        else:
            detailed_prompt = base_prompt
            ai_enhanced = False
        
        # Ultra detaylı JSON
        prompt_data = {
            "metadata": {
                "generator": "Neon Anime Prompt Generator v2.1",
                "timestamp": st.session_state.get('timestamp', '2025-08-03'),
                "version": "professional_ai_enhanced" if ai_enhanced else "professional",
                "style_category": "cyberpunk_neon_anime",
                "ai_enhanced": ai_enhanced,
                "enhancement_model": "ai_model" if ai_enhanced else None
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
            "base_prompt": base_prompt if ai_enhanced else detailed_prompt,
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
        
        if ai_enhanced:
            st.success("✅ AI ile Geliştirilmiş Ultra Detaylı Prompt Oluşturuldu! 🤖")
        else:
            st.success("✅ Ultra Detaylı Prompt Oluşturuldu!")
        
        # AI Enhancement Info - Basit gösterim
        if ai_enhanced:
            st.info("🤖 Bu prompt AI tarafından geliştirilmiştir")
            
            # Debug Information - Sadece istenirse göster
            if show_debug_info and debug_info:
                with st.expander("🔍 Teknik Detaylar (Geliştiriciler için)"):
                    # Çok basitleştirilmiş debug görünümü
                    st.markdown("### 📊 İşlem Özeti")
                    
                    col_summary1, col_summary2 = st.columns(2)
                    
                    with col_summary1:
                        api_status = debug_info.get('api_used', 'Bilinmiyor')
                        cache_hit = debug_info.get('cache_hit', False)
                        
                        if cache_hit:
                            st.success("⚡ **Hızlı İşlem:** Cache kullanıldı")
                        elif api_status in ["Primary", "Fallback"]:
                            st.info("🔄 **Canlı İşlem:** API çağrısı yapıldı")
                        else:
                            st.warning("⚠️ **API Sorunu**")
                    
                    with col_summary2:
                        original_len = debug_info.get('original_length', 0)
                        enhanced_len = debug_info.get('enhanced_length', 0)
                        improvement = enhanced_len - original_len
                        
                        if improvement > 0:
                            st.metric("Kelime Artışı", f"+{improvement}")
                        else:
                            st.metric("Kelime Sayısı", enhanced_len)
                    
                    # Sadece hata varsa göster
                    if 'error' in debug_info:
                        st.error(f"⚠️ **Hata:** {debug_info['error']}")
                        st.info("💡 **Çözüm:** API anahtarlarınızı kontrol edin.")
        
        # Sonuçları göster
        tab_names = ["🎯 Ana Prompt", "📋 Detaylı JSON", "🔄 Alternatifler", "📊 Analiz"]
        if show_debug_info and ai_enhanced:
            tab_names.append("🔧 AI Debug")
            
        tabs = st.tabs(tab_names)
        
        with tabs[0]:  # Ana Prompt
            st.subheader("🎨 DALL-E için Optimize Edilmiş Prompt:")
            
            if ai_enhanced:
                st.success("🤖 **AI ile Geliştirilmiş Prompt:**")
            else:
                st.info("📝 **Standart Prompt:**")
            
            # Kopyalama için text area
            st.text_area("📋 Kopyalamak için buradan seçin:", value=detailed_prompt, height=120, key="copy_area_main", 
                        help="Bu alanı seçip Ctrl+A ile tamamını seçin, sonra Ctrl+C ile kopyalayın")
            
            # Prompt bilgileri
            prompt_length = len(detailed_prompt.split())
            st.info(f"📏 **Toplam {prompt_length} kelime**")
            
            if ai_enhanced and base_prompt != detailed_prompt:
                with st.expander("📝 Orijinal vs AI Enhanced Karşılaştırma - Düzenleyebilirsiniz"):
                    col_comp1, col_comp2 = st.columns(2)
                    with col_comp1:
                        st.write("**Orijinal Prompt:** *(düzenlenebilir)*")
                        editable_orig = st.text_area("Orijinal prompt'u düzenleyin:", value=base_prompt, height=120, key="orig_editable", 
                                                   help="Bu metni istediğiniz gibi düzenleyebilirsiniz")
                                    
                    with col_comp2:
                        st.write("**AI Enhanced Prompt:** *(düzenlenebilir)*")
                        editable_enh = st.text_area("Enhanced prompt'u düzenleyin:", value=detailed_prompt, height=120, key="enh_editable",
                                                  help="AI tarafından geliştirilen prompt'u istediğiniz gibi düzenleyebilirsiniz")
            
        with tabs[1]:  # JSON
            st.subheader("📋 Profesyonel JSON Çıktısı:")
            st.json(prompt_data)
            
        with tabs[2]:  # Alternatifler
            st.subheader("🔄 Diğer AI Platformları için Alternatifler:")
            
            # Kısa Versiyon
            st.write("**Kısa Versiyon:**")
            st.text_area("Kopyalamak için:", value=prompt_data["alternative_prompts"]["short_version"], height=75, key="copy_short_area")
            
            # Midjourney
            st.write("**Midjourney Tarzı:**")
            st.text_area("Kopyalamak için:", value=prompt_data["alternative_prompts"]["midjourney_style"], height=75, key="copy_mj_area")
            
            # Stable Diffusion
            st.write("**Stable Diffusion:**")
            st.text_area("Kopyalamak için:", value=prompt_data["alternative_prompts"]["stable_diffusion"], height=75, key="copy_sd_area")
            
        with tabs[3]:  # Analiz
            st.subheader("📊 Prompt Analizi:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Toplam Kelime", len(detailed_prompt.split()))
                st.metric("Stil Tagları", len(prompt_data["style_tags"]))
                st.metric("Efekt Sayısı", len(effects))
                if ai_enhanced:
                    st.metric("AI Enhanced", "✅ Evet")
                else:
                    st.metric("AI Enhanced", "❌ Hayır")
            with col_b:
                st.write("**Güçlü Kelimeler:**")
                for word in prompt_data["prompt_engineering_notes"]["strength_keywords"]:
                    st.write(f"• {word}")
                if ai_enhanced:
                    st.write("**🤖 AI Geliştirme:**")
                    st.write("• AI Enhanced")
        
        # Gemini Debug Tab (only if debug is enabled and AI was used)
        if show_debug_info and ai_enhanced and len(tabs) > 4:
            with tabs[4]:  # AI Debug
                st.subheader("🔧 AI API Debug Detayları")
                
                if debug_info:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**🔗 API Bilgileri:**")
                        st.code(f"""
Model: ai-model
API Used: {debug_info.get('api_used', 'Unknown')}
Cache Hit: {debug_info.get('cache_hit', False)}
Processing Time: {debug_info.get('processing_time', 0):.3f}s
                        """)
                    
                    with col2:
                        st.write("**⚙️ Generation Config:**")
                        settings = debug_info.get('settings', {})
                        st.code(f"""
Temperature: {settings.get('creativity', 0.8)}
Max Tokens: {settings.get('max_tokens', 200)}
TopP: {min(0.95, settings.get('creativity', 0.8) + 0.1)}
TopK: {int(40 * settings.get('creativity', 0.8))}
Focus: {settings.get('focus', 'Unknown')}
                        """)
                    
                    with col3:
                        st.write("**📈 Prompt Stats:**")
                        st.code(f"""
Original Words: {debug_info.get('original_length', 0)}
Enhanced Words: {debug_info.get('enhanced_length', 0)}
Word Increase: +{debug_info.get('enhanced_length', 0) - debug_info.get('original_length', 0)}
Improvement: {((debug_info.get('enhanced_length', 0) / max(debug_info.get('original_length', 1), 1) - 1) * 100):.1f}%
                        """)
                    
                    # Show the actual prompt sent to AI
                    st.write("**📝 AI'a Gönderilen System Prompt:**")
                    focus_prompts = {
                        "Genel Artistik Kalite": "Focus on overall artistic quality, professional terminology, and visual impact",
                        "Işık ve Atmosfer": "Focus on lighting effects, atmospheric elements, and mood enhancement",
                        "Karakter Detayları": "Focus on character design, clothing details, and facial expressions",
                        "Kompozisyon ve Açılar": "Focus on camera angles, composition, and visual perspective",
                        "Malzeme ve Dokular": "Focus on materials, textures, surface details, and tactile qualities"
                    }
                    
                    focus_desc = focus_prompts.get(settings.get('focus', ''), 'Unknown focus')
                    system_prompt_display = f"""You are an expert AI art prompt engineer specializing in anime and digital art.

TASK: Enhance the given prompt to be more artistic and detailed while maintaining all core elements.

FOCUS: {focus_desc}

ENHANCEMENT RULES:
- Keep ALL original characters, settings, colors, and key descriptors
- Add 5-10 high-impact artistic enhancement words/phrases
- Use professional photography and digital art terminology
- Enhance lighting, texture, and atmospheric details
- Make descriptions more specific and vivid
- Add technical quality indicators
- Maintain the cyberpunk/neon anime aesthetic
- DO NOT add explanations or meta-commentary
- Return ONLY the enhanced prompt

Original prompt to enhance:
{base_prompt}"""
                    
                    st.code(system_prompt_display, language="text")
                else:
                    st.error("Debug bilgileri mevcut değil")
        
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
        
        # API Status
        st.markdown("---")
        api_key_1 = st.secrets.get("GEMINI_API_KEY_1", "")
        api_key_2 = st.secrets.get("GEMINI_API_KEY_2", "")
        
        if not api_key_1 and not api_key_2:
            st.subheader("🤖 AI API Durumu")
            st.error("❌ AI Enhancement disabled - No API keys configured")
        
        # Detayları göster
        if st.checkbox("Detayları Göster"):
            st.write("**Karakterler:**")
            for char, origin in st.session_state.characters.items():
                st.write(f"• {char} → {origin}")

if __name__ == "__main__":
    main()