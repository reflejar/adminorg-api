import React from 'react';
import classNames from 'classnames';
import { SectionProps } from '../../../layouts/routes/utils/SectionProps';
import ButtonGroup from '../../../components/landing/ButtonGroup';
import Button from '../../../components/landing/Button';
import Image from '../../../components/landing/Image';

import ImagenSmartCities from "../../../assets/img/smartcities/1539.jpg";

const propTypes = {
  ...SectionProps.types
}

const defaultProps = {
  ...SectionProps.defaults
}

const Hero = ({
  className,
  topOuterDivider,
  bottomOuterDivider,
  topDivider,
  bottomDivider,
  hasBgColor,
  invertColor,
  ...props
}) => {

  const outerClasses = classNames(
    'hero section center-content',
    topOuterDivider && 'has-top-divider',
    bottomOuterDivider && 'has-bottom-divider',
    hasBgColor && 'has-bg-color',
    invertColor && 'invert-color',
    className
  );

  const innerClasses = classNames(
    'hero-inner section-inner',
    topDivider && 'has-top-divider',
    bottomDivider && 'has-bottom-divider'
  );

  return (
    <section
      {...props}
      className={outerClasses}
    >
      <div className="container-sm">
        <div className={innerClasses}>
          <div className="hero-content">
            <h1 className="mt-0 mb-16 reveal-from-bottom" data-reveal-delay="200">
              Administración inteligente <span className="text-info">admin-smart</span>
            </h1>
            <div className="container-xs">
              <p className="m-0 mb-32 reveal-from-bottom" data-reveal-delay="400">
                Nuestra plataforma brinda una gestion inteligente de tu comunidad. <br />
                {/* Haciendo uso eficiente de los recursos y promoviendo ... <br />
                (aqui poner ejemplos: automatizacion de procesos, practicidad operativa, uso eficiente del tiempo, cuidado del ambiente)  */}
                </p>
              <div className="reveal-from-bottom mt-4" data-reveal-delay="600">
                <ButtonGroup>
                  <Button color="info" wideMobile href="https://cruip.com/">
                    Empeza ahora
                    </Button>
                  <Button color="dark" wideMobile href="https://github.com/cruip/open-react-template/">
                    Conoce mas de nosotros
                    </Button>
                </ButtonGroup>
              </div>
            </div>
          </div>
          <div className="hero-figure reveal-from-bottom illustration-element-01" data-reveal-value="20px" data-reveal-delay="800">
            <a
              href="#0"
            >
              <Image
                className="has-shadow"
                src={ImagenSmartCities}
                alt="Hero"
                width={896}
                height={504} />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

Hero.propTypes = propTypes;
Hero.defaultProps = defaultProps;

export default Hero;