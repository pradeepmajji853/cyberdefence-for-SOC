import React from 'react';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';
import { AlertTriangle, MapPin } from 'lucide-react';

const geoUrl = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson";

const AttackMap = ({ attackMapData }) => {
  if (!attackMapData || !attackMapData.origins) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-red-100 rounded-lg">
            <MapPin className="w-6 h-6 text-red-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Global Attack Origins</h3>
            <p className="text-sm text-gray-600">Loading attack geolocation data...</p>
          </div>
        </div>
        <div className="h-96 bg-gray-100 rounded-lg animate-pulse flex items-center justify-center">
          <span className="text-gray-500">Loading map...</span>
        </div>
      </div>
    );
  }

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical': return '#dc2626'; // red-600
      case 'high': return '#ea580c'; // orange-600
      case 'medium': return '#ca8a04'; // yellow-600
      case 'low': return '#16a34a'; // green-600
      default: return '#6b7280'; // gray-500
    }
  };

  const getMarkerSize = (attacks) => {
    if (attacks > 50) return 12;
    if (attacks > 30) return 10;
    if (attacks > 15) return 8;
    return 6;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-red-100 rounded-lg">
            <MapPin className="w-6 h-6 text-red-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Global Attack Origins</h3>
            <p className="text-sm text-gray-600">Real-time attack source visualization</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-red-600">{attackMapData.total_attacks}</div>
          <div className="text-sm text-gray-600">Total Attacks</div>
        </div>
      </div>

      <div className="h-96 mb-4">
        <ComposableMap
          projection="geoMercator"
          projectionConfig={{
            scale: 120,
            center: [0, 20],
          }}
          style={{ width: '100%', height: '100%' }}
        >
          <Geographies geography={geoUrl}>
            {({ geographies }) =>
              geographies.map((geo) => (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill="#e5e7eb"
                  stroke="#d1d5db"
                  strokeWidth={0.5}
                  style={{
                    default: { outline: 'none' },
                    hover: { fill: '#d1d5db', outline: 'none' },
                    pressed: { outline: 'none' },
                  }}
                />
              ))
            }
          </Geographies>
          
          {attackMapData.origins
            .filter(origin => origin.lat !== 0 || origin.lng !== 0) // Filter out unknown locations
            .map((origin, index) => (
            <Marker key={index} coordinates={[origin.lng, origin.lat]}>
              <circle
                r={getMarkerSize(origin.attacks)}
                fill={getSeverityColor(origin.severity)}
                fillOpacity={0.7}
                stroke="#ffffff"
                strokeWidth={1}
                style={{ cursor: 'pointer' }}
              />
              <text
                textAnchor="middle"
                y={getMarkerSize(origin.attacks) + 15}
                style={{
                  fontFamily: 'system-ui',
                  fontSize: '10px',
                  fill: '#374151',
                  fontWeight: 'bold'
                }}
              >
                {origin.attacks}
              </text>
            </Marker>
          ))}
        </ComposableMap>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-4 justify-center mb-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-600"></div>
          <span className="text-xs text-gray-600">Critical</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-orange-600"></div>
          <span className="text-xs text-gray-600">High</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-yellow-600"></div>
          <span className="text-xs text-gray-600">Medium</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-600"></div>
          <span className="text-xs text-gray-600">Low</span>
        </div>
      </div>

      {/* Top Attack Origins */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="font-medium text-gray-900 mb-3 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-red-500" />
          Top Attack Origins
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {attackMapData.origins
            .sort((a, b) => b.attacks - a.attacks)
            .slice(0, 4)
            .map((origin, index) => (
            <div key={index} className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-gray-900">
                  {origin.country === 'Unknown' ? '🌐 Unknown' : origin.country}
                </span>
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: getSeverityColor(origin.severity) }}
                ></div>
              </div>
              <div className="text-lg font-bold text-red-600">{origin.attacks}</div>
              <div className="text-xs text-gray-500 capitalize">{origin.severity} Risk</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AttackMap;
