import React from 'react';
import cs from 'classnames';

import './styles.scss';
import get from 'lodash/get';

export const AppendableRowField = ({
  data,
  fields,
  errors,
  header,
  disabled,
  appendButtonDisabled,
  popButtonDisabled,
  onAppendClick: handleAppendClick,
  onPopClick: handlePopClick,
}) => (
    <div className={cs("AppendableRowField row", { disabled })}>
      <div className="col-12 d-flex align-items-center">
        <h3 className="pl-0 credito__row__header__text">
          {header.title}
        </h3>
      </div>

      <div className="col-12">
        <div className={`AppendableRowField__fieldsrow AppendableRowField__fieldsrow--${fields.length}`}>
          {fields.map((field) => (
            <label key={field.header}>{field.header}</label>
          ))}
          {data.map((item, index) => fields.map((field) => {
            const fieldDisabled = typeof field.disabled === 'boolean'
              ? field.disabled
              : get(field, `disabled[${index}][${field.name}]`);


            return (
              <div key={field.name}>
                <div className="form-group">
                  {field.type === 'select' && (
                    <select
                      name={field.name}
                      placeholder={field.placeholder}
                      className={cs('form-control', field.className, { 'is-invalid': errors && errors[index] && errors[index][field.name] })}
                      value={item[field.name]}
                      disabled={fieldDisabled}
                      onChange={field.handleChange(index)}
                    >
                      {field.options}
                    </select>
                  )}

                  {field.type !== 'select' && (
                    <input
                      type={field.type || 'text'}
                      name={field.name}
                      placeholder={field.placeholder}
                      min={get(field, 'min', null)}
                      className={cs('form-control', field.className, { 'is-invalid': errors && errors[index] && errors[index][field.name] })}
                      value={item[field.name]}
                      checked={field.type === 'checkbox' ? item[field.name] : undefined}
                      step={field.type === 'number' ? 0.01 : ''}
                      disabled={fieldDisabled}
                      onChange={field.handleChange(index)}
                    />
                  )}

                  {errors && errors[index] && errors[index][field.name] && (
                    <div className="invalid-feedback">
                      {errors[index][field.name][0]}
                    </div>
                  )}
                </div>
              </div>
            );
          }))}
        </div>
      </div>

      {!(appendButtonDisabled && popButtonDisabled) && (
        <div className="col-12 w-100">
          <div className="d-flex justify-content-end">
            {!popButtonDisabled && (
              <button
                type="button"
                className="btn btn-danger d-block mr-2"
                onClick={handlePopClick}
                disabled={data.length <= 1}
              >
                -
              </button>
            )}

            {!appendButtonDisabled && (
              <button
                type="button"
                className="btn btn-primary d-block"
                onClick={handleAppendClick}
              >
                +
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
