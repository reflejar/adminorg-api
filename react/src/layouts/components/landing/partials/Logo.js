import React from 'react';
import classNames from 'classnames';
import { Link } from 'react-router-dom';
import Image from '../elements/Image';

import LogoAdminSmart from "../../../../assets/img/logo.png";

const Logo = ({
  className,
  ...props
}) => {

  const classes = classNames(
    'brand',
    'mt-4',
    className
  );

  return (
    <div
      {...props}
      className={classes}
    >
      <h1 className="m-0">
        <Link to="/">
          <Image
            src={LogoAdminSmart}
            alt="AdminSmart"
            width={70}
            height={70} />
        </Link>
      </h1>
    </div>
  );
}

export default Logo;