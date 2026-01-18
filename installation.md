# Installation Guide - Glow: Sun Exposure for Vitamin D

This guide provides detailed installation instructions for the Glow integration.

## Prerequisites

- Home Assistant version 2023.8.0 or later
- HACS installed (for HACS installation method)
- Home Assistant location (latitude/longitude) configured
- (Optional) UV index sensor entity available

## Method 1: HACS Installation (Recommended)

### Step 1: Add Custom Repository

1. Open Home Assistant
2. Go to **HACS** (in the sidebar)
3. Click the **three dots** (⋮) in the top right corner
4. Select **Custom repositories**
5. In the "Repository" field, paste: `https://github.com/cinghialino/glow-sun-exposure-vitamin-d`
6. In the "Category" dropdown, select: **Integration**
7. Click **Add**

### Step 2: Install the Integration

1. In HACS, search for "Glow"
2. Click on **Glow: Sun Exposure for Vitamin D**
3. Click **Download** (or **Install**)
4. Select the latest version
5. Click **Download** again to confirm

### Step 3: Restart Home Assistant

1. Go to **Settings** → **System** → **Restart**
2. Click **Restart Home Assistant**
3. Wait for Home Assistant to restart (may take 1-2 minutes)

### Step 4: Add the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for "Glow"
4. Click on **Glow: Sun Exposure for Vitamin D**

### Step 5: Configure

1. **Target Vitamin D (IU)**: Use the slider to select your daily target
   - 1000 IU: Minimal maintenance
   - 2000 IU: Standard (recommended for most people)
   - 3000-4000 IU: Higher targets

2. **UV Index Sensor** (Optional): 
   - Click the dropdown
   - Select your UV sensor if you have one (e.g., `sensor.openuv_current_uv_index`)
   - Or leave empty to use monthly averages

3. Click **Submit**

### Step 6: Verify Installation

1. Go to **Settings** → **Devices & Services**
2. Find "Glow: Sun Exposure for Vitamin D"
3. Click on it to see 6 sensor entities
4. All sensors should show a state (number of minutes, or "unknown" if sun is down)

## Method 2: Manual Installation

### Step 1: Download the Files

1. Go to https://github.com/cinghialino/glow-sun-exposure-vitamin-d
2. Click **Code** → **Download ZIP**
3. Extract the ZIP file

### Step 2: Copy Files to Home Assistant

#### Using File Editor or SSH:

1. Create the directory: `config/custom_components/glow_vitd/`
2. Copy ALL files from `custom_components/glow_vitd/` to this directory

**Required files:**
```
config/custom_components/glow_vitd/
├── __init__.py
├── config_flow.py
├── const.py
├── manifest.json
├── sensor.py
├── strings.json
└── translations/
    └── en.json
```

#### Using Samba/Network Share:

1. Connect to your Home Assistant share (e.g., `\\homeassistant.local\config`)
2. Navigate to `custom_components/`
3. Create folder `glow_vitd`
4. Copy all files from the downloaded ZIP into this folder

### Step 3: Verify File Structure

Ensure your directory looks like this:

```
/config/
  custom_components/
    glow_vitd/
      __init__.py
      config_flow.py
      const.py
      manifest.json
      sensor.py
      strings.json
      translations/
        en.json
```

### Step 4: Restart Home Assistant

1. Go to **Settings** → **System** → **Restart**
2. Wait for restart to complete

### Step 5: Add Integration

Follow **Steps 4-6** from the HACS method above.

## Verifying Your Location is Set

The integration needs your location for accurate calculations.

1. Go to **Settings** → **System** → **General**
2. Scroll to **Location**
3. Ensure **Latitude** and **Longitude** are set
4. If not set, click **Edit** and enter your coordinates

## Setting Up a UV Sensor (Optional but Recommended)

For more accurate real-time calculations, integrate a UV sensor.

### Option 1: OpenUV (Recommended)

1. Go to https://www.openuv.io/ and create a free account
2. Get your API key
3. In Home Assistant:
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration**
   - Search for "OpenUV"
   - Enter your API key
   - Configure your location
4. This creates `sensor.openuv_current_uv_index`
5. Use this sensor in Glow configuration

### Option 2: Weather Integration UV

Many weather integrations provide UV index:

- **AccuWeather**: `sensor.accuweather_uv_index`
- **Met.no**: `sensor.met_no_uv_index`
- **WeatherFlow**: `sensor.weatherflow_uv_index`

Check your weather integration's entities for UV sensors.

## Post-Installation Configuration

### Disable Unused Skin Type Sensors

If you only need certain skin types:

1. Go to **Settings** → **Devices & Services**
2. Click on **Glow: Sun Exposure for Vitamin D**
3. Click **X Entities** 
4. For each unused sensor:
   - Click the sensor
   - Click the gear icon (⚙️)
   - Toggle **Enabled** to OFF
5. Click **Update**

### Adjust Settings

To change your target IU or UV sensor:

1. Go to **Settings** → **Devices & Services**
2. Find **Glow: Sun Exposure for Vitamin D**
3. Click **Configure**
4. Adjust settings
5. Click **Submit**

## Troubleshooting Installation

### "Integration not found" Error

**Solution:**
1. Verify all files are in `config/custom_components/glow_vitd/`
2. Check file permissions (must be readable)
3. Restart Home Assistant fully
4. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)

### Sensors Show "Unavailable"

**Possible causes:**

1. **Location not set**: 
   - Go to Settings → System → General
   - Set latitude/longitude

2. **Sun integration missing**:
   - Check if `sun.sun` entity exists
   - Add Sun integration if missing

3. **Invalid UV sensor**:
   - Go to integration configuration
   - Remove or change UV sensor
   - Click Submit

### "Setup failed" Error

**Solution:**
1. Check Home Assistant logs:
   - Settings → System → Logs
   - Filter for "glow"
2. Common issues:
   - Old Home Assistant version (need 2023.8.0+)
   - Corrupted files (redownload and reinstall)
   - Permission issues (check file ownership)

### Integration Appears But Won't Configure

**Solution:**
1. Check `strings.json` and `translations/en.json` exist
2. Ensure `manifest.json` has `"config_flow": true`
3. Restart Home Assistant
4. Try clearing browser cache

### Sensors Not Updating

**Solution:**
1. Verify sun is above horizon (sensors only calculate during daytime)
2. Check if UV sensor (if configured) is available
3. Reload integration:
   - Settings → Devices & Services
   - Find Glow
   - Click "..." → Reload

## Upgrading

### Via HACS

1. Go to **HACS** → **Integrations**
2. Find **Glow: Sun Exposure for Vitamin D**
3. If update available, click **Update**
4. Restart Home Assistant
5. Check changelog for breaking changes

### Manual Upgrade

1. Download new version
2. **Backup** your current installation
3. Replace files in `custom_components/glow_vitd/`
4. Restart Home Assistant
5. Reconfigure if necessary

## Uninstallation

### Remove Integration

1. Go to **Settings** → **Devices & Services**
2. Find **Glow: Sun Exposure for Vitamin D**
3. Click **"..."** → **Delete**
4. Confirm deletion

### Remove Files (Optional)

1. Delete folder: `config/custom_components/glow_vitd/`
2. Restart Home Assistant

### Via HACS

1. Go to **HACS** → **Integrations**
2. Find **Glow: Sun Exposure for Vitamin D**
3. Click **"..."** → **Remove**
4. Also delete the integration from Devices & Services

## Getting Help

If you encounter issues:

1. **Check Logs**: Settings → System → Logs (filter: "glow")
2. **GitHub Issues**: [Report a bug](https://github.com/cinghialino/glow-sun-exposure-vitamin-d/issues)
3. **Discussions**: [Ask questions](https://github.com/cinghialino/glow-sun-exposure-vitamin-d/discussions)

When reporting issues, include:
- Home Assistant version
- Installation method (HACS or manual)
- Relevant log entries
- Steps to reproduce

## Next Steps

After successful installation:

1. Add sensor cards to your dashboard
2. Create automations for sun exposure reminders
3. Configure notification services
4. Adjust target IU based on your needs

See the main [README.md](README.md) for usage examples and automation ideas.
