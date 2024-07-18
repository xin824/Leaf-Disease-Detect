import './Header.css';
import bg from '../image/bg.jpg'
import Title from './Title';

function Header() {
  return (
    <div className='header'>
      <div>
        <img src={bg} className="App-bg"/>
      </div>
        <Title></Title>
    </div>
  );
}

export default Header;
