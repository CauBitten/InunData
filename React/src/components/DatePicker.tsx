import React from 'react';
import { DateInput, FilterControlDiv } from '../styles';

interface DatePickerProps {
    selectedDate: string;
    onDateChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    disabled: boolean;
}

const DatePicker: React.FC<DatePickerProps> = ({ selectedDate, onDateChange, disabled }) => {
    return (
        <FilterControlDiv>
            <label htmlFor="date-picker">Selecione a Data:</label>
            <DateInput
                type="date"
                id="date-picker"
                value={selectedDate}
                onChange={onDateChange}
                disabled={disabled}
            />
        </FilterControlDiv>
    );
};

export default DatePicker;