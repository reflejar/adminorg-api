import { combineReducers } from 'redux';

import lista from './list';
import search from './search';
import instance from './instance';

export default combineReducers({
  lista,
  search,
  instance
});
