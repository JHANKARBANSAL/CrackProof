const React = window.React;
const { useState, useId, useRef, useEffect } = React;
import { Icon } from "./Icon.jsx";

export const TARGET_ROLES = ["Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Java Developer", "Python Developer", "Mobile App Developer", "Data Analyst", "Data Engineer", "Data Scientist", "Machine Learning Engineer", "AI Engineer", "DevOps Engineer", "Cloud Engineer", "QA / Test Engineer", "Cybersecurity Analyst", "Product Manager", "UI / UX Designer"];

export function RolePicker({ value, onChange }) {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(-1);
  const [showAll, setShowAll] = useState(false);
  const id = useId();
  const pickerRef = useRef(null);
  useEffect(() => {
    if (open && active >= 0) pickerRef.current?.querySelectorAll('[role="option"]')[active]?.scrollIntoView({ block: "nearest" });
  }, [active, open]);
  const matches = TARGET_ROLES.filter(role => showAll || role.toLowerCase().includes(value.trim().toLowerCase()));
  const custom = value.trim() && !TARGET_ROLES.some(role => role.toLowerCase() === value.trim().toLowerCase());
  const options = [...matches, ...(custom ? [value.trim()] : [])];
  function choose(role) { onChange(role); setOpen(false); setActive(-1); }
  return <div className="role-picker" ref={pickerRef} onBlur={event => { if (!event.currentTarget.contains(event.relatedTarget)) setOpen(false); }}>
    <label htmlFor={id}>Target role <span className="required-mark">*</span></label>
    <div className="role-input"><Icon name="briefcase-business"/><input id={id} value={value} required maxLength={120} pattern=".*\S.*" placeholder="Search or enter your target role" role="combobox" aria-autocomplete="list" aria-expanded={open} aria-controls={`${id}-options`} aria-activedescendant={open && active >= 0 ? `${id}-${active}` : undefined} autoComplete="off" onFocus={() => setOpen(true)} onChange={event => { onChange(event.target.value); setShowAll(false); setOpen(true); setActive(-1); }} onKeyDown={event => {
      if (event.key === "ArrowDown" || event.key === "ArrowUp") { event.preventDefault(); setOpen(true); setActive(index => event.key === "ArrowDown" ? Math.min(index + 1, options.length - 1) : Math.max(index - 1, 0)); }
      if (event.key === "Enter" && open) { event.preventDefault(); if (options[active >= 0 ? active : 0]) choose(options[active >= 0 ? active : 0]); }
      if (event.key === "Escape") { event.preventDefault(); setOpen(false); }
    }}/><button type="button" aria-label="Show target roles" aria-expanded={open} onClick={() => { setShowAll(true); setOpen(!open); setActive(-1); }}><Icon name="chevron-down" size={18}/></button></div>
    {open && <div className="role-options" id={`${id}-options`} role="listbox" aria-label="Target roles"><div className="role-options-label" role="presentation">{value && !showAll ? "MATCHING ROLES" : "POPULAR PLACEMENT ROLES"}</div>{options.map((role, index) => <div role="option" id={`${id}-${index}`} key={role} aria-selected={index === active} onMouseDown={event => event.preventDefault()} onClick={() => choose(role)} className={index === active ? "selected" : ""}><span>{role}</span>{custom && index === options.length - 1 ? <small>Custom role</small> : <Icon name="arrow-up-right" size={15}/>}</div>)}</div>}
    <p className="field-hint">Choose a role or type your own. Your interview will adapt to this goal.</p>
  </div>;
}
