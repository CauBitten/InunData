import React from 'react';
import { Section, ChartImage } from '../styles';

interface RainfallChartProps {
    imageUrl: string;
    selectedDate: string;
}

const RainfallChart: React.FC<RainfallChartProps> = ({ imageUrl, selectedDate }) => {
    return (
        <Section>
            <h2>Chuva Acumulada por Cidade em {new Date(selectedDate).toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' })}</h2>
            <ChartImage src={imageUrl} alt="Chuva Acumulada" />
            <p>Este gráfico representaria a distribuição da chuva acumulada entre as cidades da RMR no mês selecionado.</p>
        </Section>
    );
};

export default RainfallChart;