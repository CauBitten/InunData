import React from 'react';
import { CitySelect, FilterControlDiv } from '../styles';
import { mockCities } from '../constants';

interface CitySelectorProps {
    selectedCity: string;
    onCityChange: (event: React.ChangeEvent<HTMLSelectElement>) => void;
    disabled: boolean;
}

const CitySelector: React.FC<CitySelectorProps> = ({ selectedCity, onCityChange, disabled }) => {
    return (
        <FilterControlDiv>
            <label htmlFor="city-selector">Selecione a Cidade:</label>
            <CitySelect
                id="city-selector"
                value={selectedCity}
                onChange={onCityChange}
                disabled={disabled}
            >
                {mockCities.map(city => (
                    <option key={city} value={city}>{city}</option>
                ))}
            </CitySelect>
        </FilterControlDiv>
    );
};

export default CitySelector;