import React from 'react';
import { Image } from 'react-native';
import { AppLoading, Asset } from 'expo';
import { Block, GalioProvider } from 'galio-framework';

import Screens from './navigation/Screens';
import { Images, articles, argonTheme } from './constants';
import firebase from 'firebase';

// cache app images
const assetImages = [
  Images.Onboarding,
  Images.LogoOnboarding,
  Images.Logo,
  Images.Pro,
  Images.ArgonLogo,
  Images.iOSLogo,
  Images.androidLogo
];

// cache product images
articles.map(article => assetImages.push(article.image));

function cacheImages(images) {
  return images.map(image => {
    if (typeof image === 'string') {
      return Image.prefetch(image);
    } else {
      return Asset.fromModule(image).downloadAsync();
    }
  });
}

export default class App extends React.Component {
  state = {
    isLoadingComplete: false,
  }

  // componentWillMount() {
  //   var firebaseConfig = {
  //     apiKey: "AIzaSyDEDfZim91ohoLP6ypuk0iA5ni9r3l5E-A",
  //     authDomain: "hackthenorth-2019.firebaseapp.com",
  //     databaseURL: "https://hackthenorth-2019.firebaseio.com",
  //     projectId: "hackthenorth-2019",
  //     storageBucket: "",
  //     messagingSenderId: "684933425908",
  //     appId: "1:684933425908:web:488fce1e3e243aa39c8ca1"
  //   };
  //   firebase.initializeApp(config);
  //   console.log(firebase);
  // }

  render() {
    if (!this.state.isLoadingComplete) {
      return (
        <AppLoading
          startAsync={this._loadResourcesAsync}
          onError={this._handleLoadingError}
          onFinish={this._handleFinishLoading}
        />
      );
    } else {
      return (
        <GalioProvider theme={argonTheme}>
          <Block flex>
            <Screens />
          </Block>
        </GalioProvider>
      );
    }
  }

  _loadResourcesAsync = async () => {
    return Promise.all([
      ...cacheImages(assetImages),
    ]);
  };

  _handleLoadingError = error => {
    // In this case, you might want to report the error to your error
    // reporting service, for example Sentry
    console.warn(error);
  };

  _handleFinishLoading = () => {
    this.setState({ isLoadingComplete: true });
  };

}
