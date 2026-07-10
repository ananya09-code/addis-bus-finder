type ButtonProps = {
  text: string;
  style?: string;
};

function Button({
  text,
  style = "bg-red-500 hover:bg-red-400",
}: ButtonProps) {
  return (
    <button className={`px-4 py-2 rounded-lg text-white ${style}`}>
      {text}
    </button>
  );
}

export default Button;