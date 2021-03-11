import { combineReducers } from 'redux';

import filter from './filter';
import data from './data';
import instance from './instance';
import loading from './loading';

export default combineReducers({
  filter,
  data,
  instance,
  loading
});
