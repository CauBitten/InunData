import React, { useState, useEffect } from 'react';

// Importa styled components necessários
import {
    DashboardContainer,
    Header,
    Controls,
    ContentGrid,
    Message,
    // pulse // removido, pois o botão não está visível
} from './styles';

// Importa sub-componentes
import DatePicker from './components/DatePicker';
import CitySelector from './components/CitySelector';
import RainfallChart from './components/RainfallChart';

// Importa constantes (dados mockados, etc.)
import {
    mockCities // Ainda necessário para o CitySelector
} from './constants';

const Dashboard: React.FC = () => {
    const [selectedDate, setSelectedDate] = useState('2019-12-22');
    const [selectedCity, setSelectedCity] = useState(mockCities[0]); // Padrão para a primeira cidade
    const [loading, setLoading] = useState(false);
    const [imageUrl, setImageUrl] = useState('');
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchImage = async () => {
            setLoading(true);
            setError(null);

            try {
                // Garanta que a URL corresponda ao seu endpoint de backend
                const response = await fetch(`http://localhost:8000/monthly_city_rainfall/${selectedDate}`);
                if (!response.ok) {
                    throw new Error(`Erro HTTP! Status: ${response.status} - ${response.statusText}`);
                }

                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setImageUrl(url);
            } catch (e: any) {
                console.error("Falha ao carregar imagem:", e);
                setError(`Erro ao carregar imagem: ${e.message}`);
                setImageUrl('');
            } finally {
                setLoading(false);
            }
        };

        fetchImage();
    }, [selectedDate]); // Refaz o fetch da imagem quando a data selecionada muda

    const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedDate(event.target.value);
    };

    const handleCityChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedCity(event.target.value);
    };

    return (
        <DashboardContainer>
            <Header>
                <h1>INUNDADOS</h1>
                <p>Monitoramento Integrado da Região Metropolitana do Recife</p>
            </Header>

            <Controls>
                <DatePicker
                    selectedDate={selectedDate}
                    onDateChange={handleDateChange}
                    disabled={loading}
                />
                <CitySelector
                    selectedCity={selectedCity}
                    onCityChange={handleCityChange}
                    disabled={loading}
                />
            </Controls>

            {loading && <Message type="info">Carregando dados e gerando visualizações...</Message>}
            {error && <Message type="error">{error}</Message>}

            {!loading && !error && imageUrl && (
                <ContentGrid>
                    <RainfallChart imageUrl={imageUrl} selectedDate={selectedDate} />
                </ContentGrid>
            )}
        </DashboardContainer>
    );
};

export default Dashboard;