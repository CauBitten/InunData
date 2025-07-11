import React from 'react';
import styled from 'styled-components';

const RMRAnalysisContainer = styled.div`
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
`;

const AnalysisHeader = styled.div`
    margin-bottom: 20px;
    
    h3 {
        color: #1e40af;
        margin: 0 0 8px 0;
        font-size: 1.4rem;
    }
    
    p {
        color: #64748b;
        margin: 0;
        font-size: 0.95rem;
    }
`;

const ChartContainer = styled.div`
    display: flex;
    justify-content: center;
    margin: 20px 0;
    
    img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
`;

const SummaryGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-top: 20px;
`;

const SummaryCard = styled.div`
    background: #f8fafc;
    padding: 16px;
    border-radius: 8px;
    border-left: 4px solid #3b82f6;
    
    h4 {
        margin: 0 0 8px 0;
        color: #1e40af;
        font-size: 0.9rem;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    p {
        margin: 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
    }
`;

const ErrorMessage = styled.div`
    background: #fee2e2;
    border: 1px solid #fca5a5;
    color: #dc2626;
    padding: 12px 16px;
    border-radius: 8px;
    margin: 16px 0;
`;

interface RMRAnalysisData {
    success: boolean;
    data?: {
        date: string;
        city: string;
        total_deaths: number;
        average_rain: number;
        causes: Record<string, number>;
        rmr_comparison: Record<string, any>;
        chart_image: string;
    };
    error?: string;
}

interface RMRAnalysisProps {
    data: RMRAnalysisData | null;
    loading: boolean;
}

const RMRAnalysis: React.FC<RMRAnalysisProps> = ({ data, loading }) => {
    if (loading) {
        return (
            <RMRAnalysisContainer>
                <AnalysisHeader>
                    <h3>Análise RMR</h3>
                    <p>Carregando análise de óbitos e chuva...</p>
                </AnalysisHeader>
            </RMRAnalysisContainer>
        );
    }

    if (!data) {
        return (
            <RMRAnalysisContainer>
                <AnalysisHeader>
                    <h3>Análise RMR</h3>
                    <p>Selecione uma data e cidade para ver a análise</p>
                </AnalysisHeader>
            </RMRAnalysisContainer>
        );
    }

    if (!data.success || data.error) {
        return (
            <RMRAnalysisContainer>
                <AnalysisHeader>
                    <h3>Análise RMR</h3>
                </AnalysisHeader>
                <ErrorMessage>
                    {data.error || 'Erro desconhecido'}
                </ErrorMessage>
            </RMRAnalysisContainer>
        );
    }

    const { data: analysisData } = data;

    return (
        <RMRAnalysisContainer>
            <AnalysisHeader>
                <h3>Análise RMR - {analysisData?.city}</h3>
                <p>Correlação entre óbitos e chuva para {analysisData?.date}</p>
            </AnalysisHeader>

            {analysisData?.chart_image && (
                <ChartContainer>
                    <img 
                        src={analysisData.chart_image} 
                        alt={`Análise RMR para ${analysisData.city} em ${analysisData.date}`}
                    />
                </ChartContainer>
            )}

            <SummaryGrid>
                <SummaryCard>
                    <h4>Total de Óbitos</h4>
                    <p>{analysisData?.total_deaths || 0}</p>
                </SummaryCard>
                
                <SummaryCard>
                    <h4>Chuva Média (mm)</h4>
                    <p>{analysisData?.average_rain?.toFixed(2) || '0.00'}</p>
                </SummaryCard>
                
                <SummaryCard>
                    <h4>Data da Análise</h4>
                    <p>{analysisData?.date}</p>
                </SummaryCard>
                
                <SummaryCard>
                    <h4>Cidade</h4>
                    <p>{analysisData?.city}</p>
                </SummaryCard>
            </SummaryGrid>
        </RMRAnalysisContainer>
    );
};

export default RMRAnalysis;
