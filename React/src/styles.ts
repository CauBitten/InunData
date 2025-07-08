import styled, { keyframes } from 'styled-components';

// Paleta de Cores Definida
export const colors = {
    darkNavy: '#1A2B3C', // Azul-marinho escuro (base)
    mediumNavy: '#2C4055', // Azul-marinho médio (para cards/seções)
    lightNavy: '#3D546B', // Azul-marinho claro (para detalhes)
    burntYellow: '#E0A800', // Amarelo queimado (destaque)
    lightBurntYellow: '#F2C45E', // Amarelo queimado mais claro (destaque suave)
    offWhite: '#F0F0F0', // Quase branco (texto em fundo escuro)
    lightGrey: '#A0A0A0', // Cinza claro (texto secundário)
    errorRed: '#DC3545', // Vermelho para mensagens de erro
};

// --- Efeitos Visuais (Keyframes para animações) ---

// Animação de fade-in para elementos que aparecem na tela
export const fadeIn = keyframes`
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
`;

// Animação de brilho para o botão (mantido, caso você adicione um botão no futuro)
export const pulse = keyframes`
    0% {
        box-shadow: 0 0 0 0 rgba(224, 168, 0, 0.7);
    }
    70% {
        box-shadow: 0 0 0 15px rgba(224, 168, 0, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(224, 168, 0, 0);
    }
`;

// --- Estilização com Styled Components ---

// Container principal do dashboard, centraliza e aplica estilos globais
export const DashboardContainer = styled.div`
    font-family: 'Inter', sans-serif; /* Fonte para o corpo do texto */
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px; /* Mais padding para um visual mais espaçoso */
    background: linear-gradient(135deg, ${colors.darkNavy} 0%, ${colors.mediumNavy} 100%); /* Gradiente de azul-marinho */
    min-height: 100vh;
    width: 100vw; /* Ocupa toda a largura da viewport */
    box-sizing: border-box;
    color: ${colors.offWhite}; /* Cor de texto padrão */
    overflow-x: hidden; /* Evita rolagem horizontal */
`;

// Estilização do cabeçalho principal
export const Header = styled.header`
    width: 100%;
    max-width: 1600px; /* Aumenta a largura máxima para preencher mais */
    background: linear-gradient(45deg, ${colors.darkNavy}, ${colors.mediumNavy}); /* Gradiente sutil no cabeçalho */
    color: ${colors.offWhite};
    padding: 40px 60px; /* Mais padding */
    border-radius: 25px; /* Cantos bem arredondados */
    margin-bottom: 50px; /* Mais margem inferior */
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4); /* Sombra mais forte e difusa */
    text-align: center;
    position: relative;
    overflow: hidden; /* Para garantir que o pseudo-elemento não vaze */
    animation: ${fadeIn} 1s ease-out; /* Animação de fade-in */

    h1 {
        font-family: 'Oswald', sans-serif; /* Fonte ousada para o título */
        margin: 0;
        font-size: 4.5em; /* Título ainda maior */
        letter-spacing: 3px; /* Mais espaçamento entre letras */
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3); /* Sombra no texto mais pronunciada */
        color: ${colors.burntYellow}; /* Destaque com amarelo queimado */
        position: relative;
        z-index: 1; /* Garante que o texto fique acima de qualquer efeito de fundo */
    }

    p {
        font-size: 1.3em;
        color: ${colors.lightGrey};
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }

    /* Efeito de fundo abstrato */
    &::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.05) 0%, transparent 70%);
        transform: rotate(45deg);
        opacity: 0.1;
        animation: rotateBg 20s linear infinite; /* Animação de rotação sutil */
        z-index: 0;
    }

    @keyframes rotateBg {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    @media (max-width: 1024px) {
        padding: 30px 40px;
        h1 {
            font-size: 3.5em;
        }
        p {
            font-size: 1.1em;
        }
    }
    @media (max-width: 768px) {
        padding: 25px 30px;
        h1 {
            font-size: 2.5em;
        }
        p {
            font-size: 1em;
        }
    }
    @media (max-width: 480px) {
        padding: 20px 20px;
        h1 {
            font-size: 1.8em;
        }
        p {
            font-size: 0.9em;
        }
    }
`;

// Controles de filtro (data e cidade)
export const Controls = styled.div`
    display: flex;
    flex-wrap: wrap;
    gap: 30px; /* Espaçamento maior entre os controles */
    margin-bottom: 50px; /* Mais margem inferior */
    padding: 30px; /* Mais padding */
    background-color: ${colors.mediumNavy}; /* Fundo azul-marinho médio */
    border-radius: 20px; /* Cantos arredondados */
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); /* Sombra mais forte */
    width: 100%;
    max-width: 1600px;
    justify-content: center;
    align-items: center;
    animation: ${fadeIn} 1.2s ease-out; /* Animação de fade-in */

    @media (max-width: 600px) {
        flex-direction: column;
        align-items: stretch;
    }
`;

// Grid de conteúdo para organizar seções de mapa e gráficos
export const ContentGrid = styled.div`
    display: grid;
    grid-template-columns: 1fr; /* Padrão de uma coluna para mobile */
    gap: 35px; /* Espaçamento maior entre as seções */
    width: 100%;
    max-width: 1600px;
    animation: ${fadeIn} 1.4s ease-out; /* Animação de fade-in */

    @media (min-width: 768px) {
        grid-template-columns: repeat(auto-fit, minmax(480px, 1fr)); /* 2 colunas em telas médias */
    }

    @media (min-width: 1200px) {
        grid-template-columns: repeat(auto-fit, minmax(650px, 1fr)); /* Ajuste para mais colunas em telas grandes */
    }
`;

// Estilização para cada seção individual (mapa, gráficos)
export const Section = styled.div`
    background-color: ${colors.mediumNavy}; /* Fundo azul-marinho médio */
    padding: 35px; /* Mais padding */
    border-radius: 20px; /* Cantos arredondados */
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); /* Sombra mais forte */
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 25px; /* Espaçamento entre título e conteúdo */
    transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); /* Transição suave e com curva */
    border: 1px solid rgba(255,255,255,0.05); /* Borda sutil */

    &:hover {
        transform: translateY(-8px); /* Elevação maior no hover */
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4); /* Sombra mais intensa no hover */
    }

    h2 {
        font-family: 'Oswald', sans-serif; /* Fonte ousada para títulos de seção */
        color: ${colors.lightBurntYellow}; /* Destaque com amarelo queimado mais claro */
        margin-top: 0;
        margin-bottom: 10px;
        text-align: center;
        font-size: 2.2em; /* Título de seção maior */
        font-weight: 700;
        letter-spacing: 0.8px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    p {
        color: ${colors.lightGrey}; /* Texto secundário */
        font-style: italic;
        text-align: center;
        font-size: 1.05em;
        line-height: 1.6;
    }
`;

// Wrapper para o mapa (removido, pois o mapa não é mais usado diretamente aqui)
/*
export const MapWrapper = styled.div`
    height: 600px;
    width: 100%;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    border: 2px solid ${colors.lightNavy};
    .leaflet-container {
        background-color: ${colors.darkNavy};
    }
`;
*/

// Mensagens de carregamento/erro (estilizadas)
interface MessageProps {
    type?: 'error' | 'info';
}
export const Message = styled.p<MessageProps>`
    color: ${props => (props.type === 'error' ? colors.errorRed : colors.burntYellow)}; /* Cores da paleta */
    font-weight: bold;
    text-align: center;
    margin-top: 40px;
    font-size: 1.4em; /* Fonte maior para mensagens */
    animation: ${fadeIn} 0.8s ease-out; /* Animação de fade-in */
`;

// Styled component for individual filter control div
export const FilterControlDiv = styled.div`
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
`;

// Styled input for date
export const DateInput = styled.input`
    padding: 14px 20px;
    border: 2px solid ${colors.lightNavy};
    border-radius: 12px;
    font-size: 1.1em;
    min-width: 200px;
    background-color: ${colors.darkNavy};
    color: ${colors.offWhite};
    transition: border-color 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
    appearance: none;
    cursor: pointer;

    &:focus {
        border-color: ${colors.burntYellow};
        box-shadow: 0 0 0 4px rgba(224, 168, 0, 0.3);
        outline: none;
        background-color: ${colors.lightNavy};
    }
    &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    @media (max-width: 600px) {
        width: 100%;
        min-width: unset;
    }
`;

// Styled select for city
export const CitySelect = styled.select`
    padding: 14px 20px;
    border: 2px solid ${colors.lightNavy};
    border-radius: 12px;
    font-size: 1.1em;
    min-width: 200px;
    background-color: ${colors.darkNavy};
    color: ${colors.offWhite};
    transition: border-color 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
    appearance: none;
    cursor: pointer;
    background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23F0F0F0%22%20d%3D%22M287%2C197.3L159.3%2C69.6c-3.8-3.8-10.1-3.8-13.9%2C0L5.3%2C197.3c-3.8%2C3.8-3.8%2C10.1%2C0%2C13.9l22.2%2C22.2c3.8%2C3.8%2C10.1%2C3.8%2C13.9%2C0L146.5%2C132.8c3.8-3.8%2C10.1-3.8%2C13.9%2C0l105.1%2C105.1c3.8%2C3.8%2C10.1%2C3.8%2C13.9%2C0l22.2-22.2C290.8%2C207.4%2C290.8%2C201.1%2C287%2C197.3z%22%2F%3E%3C%2Fsvg%3E');
    background-repeat: no-repeat;
    background-position: right 15px center;
    background-size: 15px;
    padding-right: 40px;

    @media (max-width: 600px) {
        width: 100%;
        min-width: unset;
    }
`;

// Styled image for charts
export const ChartImage = styled.img`
    max-width: 100%;
    height: auto;
    display: block;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.1);
`;