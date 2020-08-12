import React from 'react';
import cs from 'classnames';
import { default as ReactSelect } from 'react-select';
import './styles.scss';

export const Select = (props) => (
  <ReactSelect
    {...props}
    className={cs('Select', {
      [props.className]: props.className,
      'error': props.error
    })}
  />
);