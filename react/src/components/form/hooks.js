import { useState, useCallback } from "react"

export const useAppendableField = (initialItems, options = {}) => {
  const [fields, setFields] = useState(initialItems ? initialItems : []);

  const handleChange = useCallback((fieldIndex) => {
    if (options.custom) {
      return options.custom && options.custom.handleChange(fieldIndex);
    }

    return (event) => {
      event.persist();
      const { name, value, checked, type } = event.target;
      const val = type === 'checkbox' ? checked : value;

      const newFields = fields.map((item, i) => i === fieldIndex ? ({ ...item, [name]: val }) : item);

      setFields(newFields);
    }}, [fields, options.custom]);

  const handleAppend = useCallback(() => {
    setFields([...fields, options.cleanItem]);
  }, [fields, options.cleanItem]);

  const handlePop = useCallback(() => {
    setFields(fields.slice(0, fields.length - 1));
  }, [fields]);

  const setFieldValue = useCallback((index, values) => {
    const newFields = fields.map((item, i) => i === index ? values : item);
    setFields(newFields);
  }, [fields]);


  return [fields, handleChange, handleAppend, handlePop, setFieldValue];
}
