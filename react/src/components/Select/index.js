import React from 'react';
import cs from 'classnames';
import { default as ReactSelect } from 'react-select';
import './styles.scss';

export const Select = (props) => (
  <ReactSelect
    {...props}
    value={props.options.filter(option => option.label === props.value)}
    className={cs('Select', {
      [props.className]: props.className,
      'error': props.error
    })}
  />
);