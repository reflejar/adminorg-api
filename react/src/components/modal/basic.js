import React, { Fragment } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import PropTypes from 'prop-types';

const BasicModal = ({
  open,
  component,
  button,
  className,
  header,
  footer,
  onSubmit,
  onToggle: handleToggle,
}) => (
  <Fragment>
    <div color="danger" onClick={handleToggle}>
      {button}
    </div>

    <Modal
      size="xl"
      backdrop="static"
      isOpen={open}
      toggle={handleToggle}
      className={className}
    >

      <ModalHeader toggle={handleToggle}>
        {header}
      </ModalHeader>

      <ModalBody>
        {component}
      </ModalBody>

      {footer && (
        <ModalFooter>
          <Button color="secondary" onClick={handleToggle}>
            Cancelar
          </Button>

          <Button color="info" onClick={onSubmit}>
            Guardar
          </Button>
        </ModalFooter>
      )}
    </Modal>
  </Fragment>
);

BasicModal.propTypes = {
  button: PropTypes.element,
  className: PropTypes.string,
  header: PropTypes.string,
  component: PropTypes.element.isRequired,
  onSubmit: PropTypes.func
};

export default BasicModal;
