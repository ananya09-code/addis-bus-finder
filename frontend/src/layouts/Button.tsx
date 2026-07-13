type ButtonProps = {
  text: string;
  style?: string;
  onClick?:() => void;
};

function Button({
  text,
  style = "bg-red-500 hover:bg-red-400",
  onClick,
}: ButtonProps) {
  return (
    <button className={`px-4 py-2 rounded-lg text-white ${style}`} onClick={onClick}>
      {text}
    </button>
  );
}

export default Button;