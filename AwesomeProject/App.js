import React, { Component } from 'react';
import { Platform, StyleSheet, Text, View } from 'react-native';
import { Image } from 'react-native';

const instructions = Platform.select({
  ios: 'Press Cmd+R to reload,\n' + 'Cmd+D or shake for dev menu',
  android: 'Double tap R on your keyboard to reload,\n' + 'Shake or press menu button for dev menu',
});

let pic = {
  uri: 'https://upload.wikimedia.org/wikipedia/commons/d/de/Bananavarieties.jpg'
};

export default class App extends Component {
  render() {
    return (
      <View style={styles.container}>
        <Image source={pic} style={styles.image} />
        <Text style={styles.welcome}>Welcome to TD's Smart Spend App</Text>
        <Text style={styles.instructions}>To get started, edit App.js</Text>
        <Text style={styles.instructions}>I would thanks</Text>
        <Text style={styles.instructions}>{instructions}</Text>
      </View>
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ffffff',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
  image: {
    width: '100%',
    height: '85%',
    position: 'relative',
    top: 0,
  }
});
