# ⚡ Neon Anime Prompt Generator

A powerful Streamlit application for generating detailed, professional-quality prompts for AI image generation platforms like DALL-E, Midjourney, and Stable Diffusion.

## 🌐 Try It Live!

**[✨ Launch the App](https://prompt-generator-ymcbzrgn.streamlit.app/)** - No installation required!

## 🚀 Features

- **Character Library**: Pre-loaded cyberpunk and anime characters with their origin worlds
- **Dynamic Poses**: 10+ action-packed poses with energy effects
- **Color Palettes**: Curated cyberpunk color schemes (Cyberpunk Classic, Neon Sunset, Ice Fire, Toxic Glow)
- **Art Styles**: Professional anime and digital art styles
- **Lighting Systems**: Dramatic neon and cinematic lighting options
- **Backgrounds**: Dark, minimalist backgrounds perfect for neon aesthetics
- **Mood & Expression**: Character personality and atmospheric settings
- **Multi-Platform Output**: Optimized prompts for different AI platforms
- **💾 Persistent Storage**: Your custom additions are automatically saved and persist across sessions
- **🤖 AI Enhancement**: Gemini Flash 2.0 integration for intelligent prompt optimization
- **⚡ Smart Caching**: Minimal API usage with intelligent caching system
- **🔄 Fallback API**: Dual API key support for 99.9% uptime

## 🎯 Generated Output

The app creates:
- **DALL-E Optimized Prompts**: Detailed, keyword-rich prompts
- **Professional JSON**: Complete metadata and technical specifications
- **Alternative Formats**: Midjourney and Stable Diffusion compatible prompts
- **Prompt Analysis**: Word count, style tags, and strength keywords

## 🛠️ Installation

### Option 1: Try Online (Recommended)
Simply visit **[https://prompt-generator-ymcbzrgn.streamlit.app/](https://prompt-generator-ymcbzrgn.streamlit.app/)** - no setup required!

### Option 2: Run Locally
1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install streamlit requests
   ```
3. (Optional) Configure Gemini API keys for AI enhancement:
   - Get API keys from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add them to `.streamlit/secrets.toml` (see example file)
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🚀 Usage

### Quick Start
1. **[Open the live app](https://prompt-generator-ymcbzrgn.streamlit.app/)**
2. Choose your mode:
   - **🎨 Prompt Oluştur**: Generate prompts using existing elements
   - **➕ Öğe Ekle**: Add new characters, poses, colors, and styles

### For Local Installation
1. Run the application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to the provided local URL (usually `http://localhost:8501`)

### Using the Generator
1. Choose your mode from the sidebar
2. Select your preferences:
   - Character and pose
   - Color palette and art style
   - Lighting and background
   - Mood and expression
   - Visual effects (optional)

3. **🤖 AI Enhancement (Optional)**: Toggle AI enhancement to use Gemini Flash 2.0 for intelligent prompt optimization

4. Click **"🎨 ULTRA PROMPT OLUŞTUR"** to generate your professional prompt

## 🤖 AI Enhancement

### Gemini Flash 2.0 Integration
- **Smart Enhancement**: AI automatically improves your prompts for better results
- **Minimal Token Usage**: Optimized API calls with maximum 150 tokens output
- **Smart Caching**: Similar prompts are cached to reduce API usage by 80%
- **Dual API Support**: Primary and fallback API keys for maximum reliability
- **Cost Effective**: Gemini Flash 2.0 is extremely affordable (virtually free for this usage)

### Setup (Optional)
1. Get free API keys from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add keys to Streamlit Cloud secrets or local `.streamlit/secrets.toml`
3. **Important**: Never commit `secrets.toml` to git (already in `.gitignore`)
4. Enjoy AI-enhanced prompts with before/after comparison

## 📋 Example Output

```
masterpiece, best quality, ultra detailed, anime style digital art, cyberpunk hacker girl from neon-lit server room, confident and determined expression, dynamic crouched pose ready to strike with glowing weapon, dramatic neon lighting with strong rim lighting creating dramatic shadows, pure black background, electric blue, hot pink, neon purple, cyan with glowing edges and neon accents, soft outer glow, volumetric lighting, dark and mysterious atmosphere, sharp focus, perfect composition, cinematic quality
```

## 🎨 Customization

### Adding New Elements

Use the **"➕ Öğe Ekle"** tab to add:
- **Characters**: Name and origin world
- **Poses**: Detailed action descriptions
- **Color Palettes**: Named color schemes
- **Art Styles**: Artistic techniques and styles
- **Lighting**: Lighting effects and moods
- **Backgrounds**: Environmental settings
- **Moods/Expressions**: Character emotions and atmospheres

### Session Persistence

All added elements are automatically saved to a JSON file and will persist across browser sessions, page refreshes, and app restarts. Your custom content is preserved!

## 🎯 Target Platforms

- **DALL-E 3**: Main optimized output
- **Midjourney**: Alternative format with aspect ratio
- **Stable Diffusion**: Weight-optimized format
- **Any AI Image Generator**: Professional quality descriptions

## 📊 Technical Features

- **Session State Management**: Persistent data across interactions
- **File-Based Storage**: JSON persistence that survives app restarts
- **Automatic Save**: All additions are automatically saved to disk
- **AI Integration**: Gemini Flash 2.0 API with intelligent caching
- **Fallback System**: Dual API keys for maximum uptime
- **Token Optimization**: Minimal API usage with smart prompt engineering
- **Tabbed Interface**: Organized input sections
- **Real-time Updates**: Immediate addition of new elements
- **Professional JSON**: Structured output with metadata
- **Responsive Design**: Works on desktop and mobile

## 🛡️ Requirements

- Python 3.7+
- Streamlit
- Modern web browser

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements:
- New character archetypes
- Additional art styles
- Enhanced color palettes
- Better prompt engineering techniques

---

**Made with ⚡ for the cyberpunk anime community**
