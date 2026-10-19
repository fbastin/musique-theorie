\version "2.24.3"
%% Fichier produit par outils/generer_tonalites.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new Staff  {
      \clef treble \time 4/4 \override TextScript.staff-padding = #2.5 \key c \major
      c''4_\markup \small \italic "do majeur" d''4 e''4 f''4 | g''4 e''4 c''4 e''4 | d''4_\markup \small \italic "la mineur" b'4 \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) \tweak Accidental.color #(rgb-color 0.588 0.157 0.118) gis'4 b'4 | a'1
      \bar "|." 
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
