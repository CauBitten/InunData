import styled, { keyframes } from 'styled-components';

// Paleta de Cores Definida
export const colors = {
    darkNavy: '#1A2B3C', // Azul-marinho escuro (base)
    mediumNavy: '#2C4055', // Azul-marinho médio (para cards/seções)
    lightNavy: '#3D546B', // Azul-marinho claro (para detalhes e bordas)
    burntYellow: '#E0A800', // Amarelo queimado (destaque principal)
    lightBurntYellow: '#F2C45E', // Amarelo queimado mais claro (destaque suave)
    offWhite: '#F0F0F0', // Quase branco (texto em fundo escuro)
    lightGrey: '#A0A0A0', // Cinza claro (texto secundário)
    errorRed: '#DC3545', // Vermelho para mensagens de erro
};

// --- Efeitos Visuais (Keyframes para animações) ---
// Mantendo apenas o fade-in para a aparição suave dos elementos
export const fadeIn = keyframes`
    from {
        opacity: 0;
        transform: translateY(10px); /* Suavemente para cima */
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
`;

// A animação de brilho 'pulse' foi removida, pois sugere uma "frescura" visual.

// --- Estilização com Styled Components ---

// Container principal do dashboard
export const DashboardContainer = styled.div`
    font-family: 'Inter', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px; /* Padding reduzido para um look mais clean */
    background-color: ${colors.darkNavy}; /* Fundo sólido e escuro */
    min-height: 100vh;
    width: 100vw;
    box-sizing: border-box;
    color: ${colors.offWhite};
    overflow-x: hidden;
`;

// Estilização do cabeçalho principal
export const Header = styled.header`
    width: 100%;
    max-width: 1200px; /* Largura máxima um pouco menor */
    background-color: ${colors.mediumNavy}; /* Fundo sólido */
    color: ${colors.offWhite};
    padding: 30px 40px; /* Padding simplificado */
    border-radius: 15px; /* Cantos arredondados, mas não tão exagerados */
    margin-bottom: 40px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Sombra mais sutil */
    text-align: center;
    animation: ${fadeIn} 0.8s ease-out; /* Animação de fade-in */

    h1 {
        font-family: 'Oswald', sans-serif;
        margin: 0;
        font-size: 3.5em; /* Tamanho do título reduzido para ser menos "gritante" */
        letter-spacing: 1px; /* Espaçamento de letras mais sutil */
        text-shadow: none; /* Sombra no texto removida */
        color: ${colors.burntYellow};
    }

    p {
        font-size: 1.1em;
        color: ${colors.lightGrey};
        margin-top: 5px; /* Margem ajustada */
    }

    // Efeito de fundo abstrato e animação de rotação removidos.

    @media (max-width: 1024px) {
        padding: 25px 30px;
        h1 {
            font-size: 3em;
        }
        p {
            font-size: 1em;
        }
    }
    @media (max-width: 768px) {
        padding: 20px 25px;
        h1 {
            font-size: 2.2em;
        }
        p {
            font-size: 0.9em;
        }
    }
    @media (max-width: 480px) {
        padding: 15px 20px;
        h1 {
            font-size: 1.6em;
        }
        p {
            font-size: 0.8em;
        }
    }
`;

// Controles de filtro (data e cidade)
export const Controls = styled.div`
    display: flex;
    flex-wrap: wrap;
    gap: 20px; /* Espaçamento reduzido */
    margin-bottom: 40px;
    padding: 20px; /* Padding reduzido */
    background-color: ${colors.mediumNavy};
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    width: 100%;
    max-width: 1200px;
    justify-content: center;
    align-items: center;
    animation: ${fadeIn} 1s ease-out; /* Animação de fade-in */

    @media (max-width: 600px) {
        flex-direction: column;
        align-items: stretch;
    }
`;

// Grid de conteúdo para organizar seções de gráficos
export const ContentGrid = styled.div`
    display: grid;
    grid-template-columns: 1fr;
    gap: 25px; /* Espaçamento reduzido */
    width: 100%;
    max-width: 1200px;
    animation: ${fadeIn} 1.2s ease-out; /* Animação de fade-in */

    @media (min-width: 768px) {
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); /* Ajuste para menos colunas em telas médias */
    }

    @media (min-width: 1024px) {
        grid-template-columns: 1fr; /* Mantenha uma coluna para o gráfico principal se for o único */
    }
`;

// Estilização para cada seção individual (gráfico)
export const Section = styled.div`
    background-color: ${colors.mediumNavy};
    padding: 25px; /* Padding reduzido */
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px; /* Espaçamento reduzido */
    transition: none; /* Transições removidas para simplificar */
    border: 1px solid ${colors.lightNavy}; /* Borda mais visível e simples */

    // Efeitos de hover e outras transições complexas removidas.

    h2 {
        font-family: 'Oswald', sans-serif;
        color: ${colors.lightBurntYellow};
        margin-top: 0;
        margin-bottom: 5px;
        text-align: center;
        font-size: 1.8em; /* Título de seção menor */
        font-weight: 600;
        letter-spacing: 0.5px;
        text-shadow: none; /* Sombra no texto removida */
    }
    p {
        color: ${colors.lightGrey};
        font-style: normal; /* Itálico removido */
        text-align: center;
        font-size: 0.95em;
        line-height: 1.5;
    }
`;

// Mensagens de carregamento/erro
interface MessageProps {
    type?: 'error' | 'info';
}
export const Message = styled.p<MessageProps>`
    color: ${props => (props.type === 'error' ? colors.errorRed : colors.burntYellow)};
    font-weight: bold;
    text-align: center;
    margin-top: 30px;
    font-size: 1.2em; /* Fonte menor */
    animation: ${fadeIn} 0.6s ease-out;
`;

// Styled component for individual filter control div
export const FilterControlDiv = styled.div`
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px; /* Espaçamento ainda menor */
`;

// Styled input for date
export const DateInput = styled.input`
    padding: 10px 15px; /* Padding reduzido */
    border: 1px solid ${colors.lightNavy}; /* Borda mais fina e simples */
    border-radius: 8px; /* Cantos menos arredondados */
    font-size: 1em;
    min-width: 180px; /* Largura mínima ajustada */
    background-color: ${colors.darkNavy};
    color: ${colors.offWhite};
    transition: border-color 0.2s ease, box-shadow 0.2s ease; /* Transições simplificadas */
    appearance: none;
    cursor: pointer;

    &:focus {
        border-color: ${colors.burntYellow};
        box-shadow: 0 0 0 2px rgba(224, 168, 0, 0.2); /* Sombra mais sutil no foco */
        outline: none;
        background-color: ${colors.lightNavy};
    }
    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    @media (max-width: 600px) {
        width: 100%;
        min-width: unset;
    }
`;

// Styled select for city
export const CitySelect = styled.select`
    padding: 10px 15px; /* Padding reduzido */
    border: 1px solid ${colors.lightNavy}; /* Borda mais fina e simples */
    border-radius: 8px; /* Cantos menos arredondados */
    font-size: 1em;
    min-width: 180px; /* Largura mínima ajustada */
    background-color: ${colors.darkNavy};
    color: ${colors.offWhite};
    transition: border-color 0.2s ease, box-shadow 0.2s ease; /* Transições simplificadas */
    appearance: none;
    cursor: pointer;
    // Icone da seta simplificado, com cor base no offWhite
    background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23F0F0F0%22%20d%3D%22M287%2C197.3L159.3%2C69.6c-3.8-3.8-10.1-3.8-13.9%2C0L5.3%2C197.3c-3.8%2C3.8-3.8%2C10.1%2C0%2C13.9l22.2%2C22.2c3.8%2C3.8%2C10.1%2C3.8%2C13.9%2C0L146.5%2C132.8c3.8-3.8%2C10.1-3.8%2C13.9%2C0l105.1%2C105.1c3.8%2C3.8%2C10.1%2C3.8%2C13.9%2C0l22.2-22.2C290.8%2C207.4%2C290.8%2C201.1%2C287%2C197.3z%22%2F%3E%3C%2Fsvg%3E');
    background-repeat: no-repeat;
    background-position: right 10px center; /* Posição ajustada */
    background-size: 12px; /* Tamanho da seta menor */
    padding-right: 30px; /* Espaço para a seta ajustado */

    &:focus {
        border-color: ${colors.burntYellow};
        box-shadow: 0 0 0 2px rgba(224, 168, 0, 0.2);
        outline: none;
        background-color: ${colors.lightNavy};
    }
    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

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
    border-radius: 8px; /* Cantos menos arredondados */
    box-shadow: 0 2px 8px rgba(0,0,0,0.15); /* Sombra mais leve */
    border: 1px solid ${colors.lightNavy}; /* Borda mais fina e simples */
`;