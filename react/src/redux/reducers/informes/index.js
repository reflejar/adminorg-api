import { combineReducers } from 'redux';

import filter from './filter';
import data from './data';
import instance from './instance';

export default combineReducers({
  filter,
  data,
  instance
});
