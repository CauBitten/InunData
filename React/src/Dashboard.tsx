import React, { useState, useEffect } from 'react';

import {
    DashboardContainer,
    Header,
    Controls,
    ContentGrid,
    Message,
} from './styles';

import DatePicker from './components/DatePicker';
import CitySelector from './components/CitySelector';
import RainfallChart from './components/RainfallChart';
import RMRChart from './components/RMRChart';

// Importa constantes (dados mockados, etc.)
import {
    // Ainda necessário para o CitySelector
    mockCities 
} from './constants';

const Dashboard: React.FC = () => {
    const [selectedDate, setSelectedDate] = useState('2019-12-22');
    const [selectedCity, setSelectedCity] = useState(mockCities[0]); // Padrão para a primeira cidade
    const [loading, setLoading] = useState(false);
    const [imageUrl, setImageUrl] = useState('');
    const [error, setError] = useState<string | null>(null);
    
    // Novo estado para o gráfico RMR
    const [rmrLoading, setRmrLoading] = useState(false);
    const [rmrImageUrl, setRmrImageUrl] = useState('');
    const [rmrError, setRmrError] = useState<string | null>(null);

    useEffect(() => {
        const fetchImage = async () => {
            setLoading(true);
            setError(null);

            try {
                const response = await fetch(`http://localhost:8000/monthly_city_rainfall/${selectedDate}`);
                if (!response.ok) {
                    throw new Error(`Erro HTTP! Status: ${response.status} - ${response.statusText}`);
                }

                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setImageUrl(url);
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
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

    // Função para buscar gráfico RMR
    useEffect(() => {
        const fetchRMRImage = async () => {
            setRmrLoading(true);
            setRmrError(null);

            try {
                const response = await fetch(`http://localhost:8000/comparar_rmr_dia/${selectedDate}/${selectedCity}`);
                if (!response.ok) {
                    throw new Error(`Erro HTTP! Status: ${response.status} - ${response.statusText}`);
                }

                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setRmrImageUrl(url);
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            } catch (e: any) {
                console.error("Falha ao carregar gráfico RMR:", e);
                setRmrError(`Erro ao carregar gráfico RMR: ${e.message}`);
                setRmrImageUrl('');
            } finally {
                setRmrLoading(false);
            }
        };

        fetchRMRImage();
    }, [selectedDate, selectedCity]); // Refaz o fetch quando data ou cidade mudam

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

            {/* Seção do Gráfico RMR */}
            {!rmrLoading && !rmrError && rmrImageUrl && (
                <ContentGrid>
                    <RMRChart 
                        imageUrl={rmrImageUrl}
                        selectedDate={selectedDate}
                        selectedCity={selectedCity}
                        loading={rmrLoading}
                    />
                </ContentGrid>
            )}

            {rmrLoading && <Message type="info">Carregando análise RMR...</Message>}
            {rmrError && <Message type="error">{rmrError}</Message>}
        </DashboardContainer>
    );
};

export default Dashboard;