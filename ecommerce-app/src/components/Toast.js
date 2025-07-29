import Toast from 'react-bootstrap/Toast';

function ToastMsg({msg, show, onClose}) {
  return (
    <Toast show={show} onClose={onClose} delay={3000} autohide>
      <Toast.Header>
        <img src="holder.js/20x20?text=%20" className="rounded me-2" alt="" />
        <strong className="me-auto">Success!</strong>
        <small>Just now</small>
      </Toast.Header>
      <Toast.Body>The Product: {msg} has been added to your cart.</Toast.Body>
    </Toast>
  );
}

export default ToastMsg;