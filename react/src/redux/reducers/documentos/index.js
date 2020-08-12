import { combineReducers } from 'redux';

import list from './list';
import instance from './instance';

export default combineReducers({
  list,
  instance
});
