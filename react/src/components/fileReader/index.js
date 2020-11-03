import React from 'react';
import FileViewer from 'react-file-viewer';

const FileReader = ({ file }) => {
    const separator = file.split(".");
    const type = separator[separator.length - 1]
  
    return (
      <FileViewer
        fileType={type}
        filePath={file}/>
    );

}
  
export default FileReader;
  