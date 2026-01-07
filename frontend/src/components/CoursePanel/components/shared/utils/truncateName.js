export const truncateName = (text, limit = 20) => {
  if (!text) return '';
  return text.length > limit ? text.slice(0, limit) + '…' : text;
};


