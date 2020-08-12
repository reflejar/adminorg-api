export const mapToOptions = (options) => {
  if (!Array.isArray(options) || options.length === 0) {
      return [];
  }

  return options.map((option) => ({
      value: option.id,
      label: option.nombre || option.name
  }));
};
