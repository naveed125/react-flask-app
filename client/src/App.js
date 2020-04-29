import React from 'react';
import './App.css';

class App extends React.Component {

  constructor(props) {

    super(props)

    this.state = {
        success: false,
        quote: "Loading..."
    }

    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  getNewQuoteFromServer() {

      fetch("http://localhost:5000/quote")
        .then(res => res.json())
        .then(
            (result) => {
                this.setState ({
                    success: false,
                    quote: result.quote + " - Einstein."
                })
            },
            (error) => {
                this.setState({
                    success: true,
                    quote: "Failed to get data. " + error
                })
            }
        )
  }

  componentDidMount() {
    this.getNewQuoteFromServer()
  }

  handleClick(e) {
    this.getNewQuoteFromServer()
  }

  render() {

      return (
        <div className="App" onClick={this.handleClick}>
              {this.state.quote}
        </div>
      );
  }

}

export default App;
