import React from 'react';
import { Section, ChartImage } from '../styles';

interface RMRChartProps {
    imageUrl: string;
    selectedDate: string;
    selectedCity: string;
    loading: boolean;
}

const RMRChart: React.FC<RMRChartProps> = ({ imageUrl, selectedDate, selectedCity, loading }) => {
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('pt-BR', { 
            day: 'numeric',
            month: 'long', 
            year: 'numeric' 
        });
    };

    return (
        <Section>
            <h2>Análise de Óbitos e Chuvas na RMR</h2>
            <p>
                Comparação diária de óbitos por causas relacionadas a acidentes (CID-W) e precipitação pluviométrica para <strong>{selectedCity}</strong> em {formatDate(selectedDate)}
            </p>
            {loading ? (
                <div style={{ 
                    display: 'flex', 
                    justifyContent: 'center', 
                    alignItems: 'center', 
                    height: '200px',
                    color: '#A0A0A0'
                }}>
                    Carregando análise RMR...
                </div>
            ) : (
                <ChartImage 
                    src={imageUrl} 
                    alt={`Análise RMR para ${selectedCity} em ${formatDate(selectedDate)}`}
                />
            )}
            <p>
                Este gráfico apresenta a correlação entre eventos pluviométricos e registros de óbitos por causas acidentais na Região Metropolitana do Recife, destacando {selectedCity} em comparação com as demais cidades.
            </p>
        </Section>
    );
};

export default RMRChart;
