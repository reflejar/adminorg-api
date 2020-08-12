import { combineReducers } from 'redux';

import list from './list';
import search from './search';
import instance from './instance';

export default combineReducers({
  list,
  search,
  instance
});
