import React from 'react';
import styled from 'styled-components';

interface MapViewerProps {
  selectedDate: string;
  loading?: boolean;
}

const MapIframe = styled.iframe`
  width: 100%;
  height: 100%;
  min-height: 500px;
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
    return <LoadingMessage>Carregando mapa interativo...</LoadingMessage>;
  }

  return (
    <MapIframe
      src={mapUrl}
      title={`Mapa RMR - ${selectedDate}`}
      onLoad={() => console.log('Mapa carregado')}
      onError={() => console.error('Erro ao carregar mapa')}
    />
  );
};

export default MapViewer;
