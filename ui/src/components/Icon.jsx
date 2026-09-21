const React = window.React;
export function Icon({ name, size = 20, className = "" }) {
  return <img className={`ui-icon ${className}`} src={`/Images/icons/${name}.svg`} alt="" aria-hidden="true" width={size} height={size} />;
}
