import L from 'leaflet';

// Corrige o problema de ícone padrão do Leaflet em ambientes como Webpack/Vite
// Isso garante que os marcadores do mapa sejam exibidos corretamente
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

// Lista de cidades mockadas para o seletor
export const mockCities = [
    'Recife', 'Jaboatão dos Guararapes', 'Olinda', 'Paulista',
    'Cabo de Santo Agostinho', 'Camaragibe', 'São Lourenço da Mata',
    'Igarassu', 'Abreu e Lima', 'Ipojuca', 'Moreno', 'Araçoiaba',
    'Itapissuma', 'Itamaracá'
];