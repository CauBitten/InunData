import React from 'react';
import styled from 'styled-components';

interface MapViewerProps {
  selectedDate: string;
  loading?: boolean;
}

const MapContainer = styled.div`
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
`;

const MapTitle = styled.h2`
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.5rem;
`;

const MapIframe = styled.iframe`
  width: 100%;
  height: 600px;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const LoadingMessage = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #7f8c8d;
  font-size: 1.1rem;
`;



const MapViewer: React.FC<MapViewerProps> = ({ selectedDate, loading = false }) => {
  const mapUrl = `http://localhost:8000/mapa_rmr/${selectedDate}`;

  if (loading) {
    return (
      <MapContainer>
        <MapTitle>Mapa da RMR - Mortalidade e Pluviometria</MapTitle>
        <LoadingMessage>Carregando mapa interativo...</LoadingMessage>
      </MapContainer>
    );
  }

  return (
    <MapContainer>
      <MapTitle>
        Mapa da RMR - Mortalidade e Pluviometria
        <br />
        <small style={{ color: '#7f8c8d', fontSize: '0.8rem' }}>
          Data: {new Date(selectedDate).toLocaleDateString('pt-BR')}
        </small>
      </MapTitle>
      <MapIframe
        src={mapUrl}
        title={`Mapa RMR - ${selectedDate}`}
        onLoad={() => console.log('Mapa carregado')}
        onError={() => console.error('Erro ao carregar mapa')}
      />
    </MapContainer>
  );
};

export default MapViewer;
