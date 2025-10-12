# Air Quality Dashboard

This directory contains the HTML, CSS, and TypeScript/JavaScript implementation of the Air Quality Dashboard, translated from the original React TSX component.

## File Structure

```
dashboard/src/
├── html/
│   └── dashboard.html          # Main HTML file
├── style/
│   └── dashboard.css          # CSS styles with Safari compatibility
├── scripts/
│   ├── dashboard.js           # Compiled JavaScript (ready to use)
│   ├── dashboard.ts           # TypeScript source
│   └── dashboard.d.ts         # TypeScript declarations
```

## Features

- **Interactive Map**: Netherlands provinces with hover effects and AQI color coding
- **City Markers**: Air quality monitoring stations with animated indicators
- **Province Tooltips**: Detailed information on hover
- **Stations List**: Sidebar with all monitoring stations
- **Responsive Design**: Works on desktop and mobile devices
- **Safari Compatible**: Includes webkit prefixes for backdrop-filter

## Dependencies

The dashboard uses D3.js for map rendering and data visualization:

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="https://d3js.org/topojson.v3.min.js"></script>
```

## Usage

1. Open `dashboard.html` in a web browser
2. The dashboard will automatically load and render the map
3. Hover over provinces to see detailed information
4. City markers show individual station data

## Browser Support

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (with webkit prefixes)
- Mobile browsers: Responsive design included

## Data Structure

The dashboard uses the following data structure for regions:

```javascript
{
    name: 'Amsterdam',
    coordinates: [4.9041, 52.3676], // [longitude, latitude]
    aqi: 45,
    status: 'good',
    province: 'Noord-Holland'
}
```

## AQI Color Coding

- **Good (0-50)**: Green (#10b981)
- **Moderate (51-100)**: Yellow (#fbbf24)
- **Unhealthy (101-150)**: Orange (#f97316)
- **Hazardous (151+)**: Red (#ef4444)

## Customization

To modify the dashboard:

1. **Add new regions**: Update the `regions` array in `dashboard.js`
2. **Change colors**: Modify the `getAQIColor()` function
3. **Update styling**: Edit `dashboard.css`
4. **TypeScript development**: Use `dashboard.ts` and compile to JavaScript

## Development

If using TypeScript:

```bash
# Install TypeScript compiler
npm install -g typescript

# Compile TypeScript to JavaScript
tsc dashboard.ts --target es2017 --lib dom,es2017
```

## Map Data

The dashboard uses Netherlands province boundaries from:
- Source: Natural Earth via TopoJSON
- URL: https://raw.githubusercontent.com/deldersveld/topojson/master/countries/netherlands/netherlands-provinces.json

## Performance Notes

- Map data is cached after first load
- SVG rendering is optimized for performance
- Responsive breakpoints minimize layout shifts
- CSS animations use hardware acceleration