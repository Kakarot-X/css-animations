import { useEffect, useRef } from "react";

const AnimationPreview = ({ cssCode, shape, isPlaying, small = false }) => {
  const styleRef = useRef(null);

  useEffect(() => {
    if (styleRef.current) {
      styleRef.current.textContent = cssCode;
    }
  }, [cssCode]);

  const getShapeStyle = () => {
    const baseSize = small ? '80px' : '120px';
    
    const styles = {
      cube: {
        width: baseSize,
        height: baseSize,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: '8px',
      },
      square: {
        width: baseSize,
        height: baseSize,
        background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        borderRadius: '0',
      },
      circle: {
        width: baseSize,
        height: baseSize,
        background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        borderRadius: '50%',
      },
      rectangle: {
        width: small ? '120px' : '160px',
        height: baseSize,
        background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        borderRadius: '8px',
      },
    };

    return styles[shape] || styles.cube;
  };

  return (
    <div className="flex items-center justify-center" style={{ minHeight: small ? '120px' : '200px' }}>
      <style ref={styleRef}></style>
      <div
        className="animated-element"
        data-testid="animation-preview"
        style={{
          ...getShapeStyle(),
          animationPlayState: isPlaying ? 'running' : 'paused',
        }}
      />
    </div>
  );
};

export default AnimationPreview;
